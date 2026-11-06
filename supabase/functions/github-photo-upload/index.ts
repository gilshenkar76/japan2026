import "@supabase/functions-js/edge-runtime.d.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
};

const owner = Deno.env.get("GITHUB_REPO_OWNER") || "gilshenkar76";
const repo = Deno.env.get("GITHUB_REPO_NAME") || "japan2026";
const branch = Deno.env.get("GITHUB_REPO_BRANCH") || "master";
const photoFolder = Deno.env.get("GITHUB_PHOTO_FOLDER") || "trip-photos";
const maxFileBytes = 12 * 1024 * 1024;
const maxBatchBytes = 24 * 1024 * 1024;
const allowedTypes = new Set(["image/jpeg", "image/png", "image/webp", "image/gif", "image/avif"]);

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

function githubHeaders(token: string) {
  return {
    Accept: "application/vnd.github+json",
    Authorization: `Bearer ${token}`,
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
  };
}

async function github(path: string, token: string, init: RequestInit = {}) {
  const response = await fetch(`https://api.github.com/repos/${owner}/${repo}${path}`, {
    ...init,
    headers: { ...githubHeaders(token), ...(init.headers || {}) },
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`GitHub ${response.status}: ${detail.slice(0, 500)}`);
  }
  return response.status === 204 ? null : response.json();
}

function safeName(name: string) {
  const extension = name.toLowerCase().match(/\.(jpe?g|png|webp|gif|avif)$/)?.[0] || ".jpg";
  const stem = name.replace(/\.[^.]+$/, "").normalize("NFKD").replace(/[^a-zA-Z0-9_-]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 55) || "photo";
  return `${stem}${extension === ".jpeg" ? ".jpg" : extension}`;
}

function bytesToBase64(bytes: Uint8Array) {
  let binary = "";
  const chunkSize = 0x8000;
  for (let offset = 0; offset < bytes.length; offset += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + chunkSize));
  }
  return btoa(binary);
}

async function listPhotos(token: string) {
  const tree = await github(`/git/trees/${encodeURIComponent(branch)}?recursive=1`, token);
  const prefix = `${photoFolder}/`;
  const photos = (tree?.tree || [])
    .filter((item: { type?: string; path?: string }) => item.type === "blob" && item.path?.startsWith(prefix) && /\.(jpe?g|png|webp|gif|avif)$/i.test(item.path))
    .map((item: { path: string; sha: string; size?: number }) => ({
      path: item.path,
      name: item.path.split("/").pop(),
      sha: item.sha,
      size: item.size || 0,
      url: `https://raw.githubusercontent.com/${owner}/${repo}/${branch}/${item.path.split("/").map(encodeURIComponent).join("/")}`,
    }))
    .sort((first: { path: string }, second: { path: string }) => second.path.localeCompare(first.path));
  return photos;
}

async function uploadPhotos(request: Request, token: string, email: string) {
  const form = await request.formData();
  const files = form.getAll("photos").filter((value): value is File => value instanceof File);
  if (!files.length) return json({ error: "No photos supplied" }, 400);
  if (files.length > 12) return json({ error: "Up to 12 photos can be uploaded at once" }, 400);

  let totalBytes = 0;
  for (const file of files) {
    totalBytes += file.size;
    if (!allowedTypes.has(file.type)) return json({ error: `${file.name}: unsupported image format` }, 400);
    if (file.size > maxFileBytes) return json({ error: `${file.name}: maximum size is 12 MB` }, 400);
  }
  if (totalBytes > maxBatchBytes) return json({ error: "The selected batch exceeds 24 MB" }, 400);

  const ref = await github(`/git/ref/heads/${encodeURIComponent(branch)}`, token);
  const parentSha = ref.object.sha;
  const parentCommit = await github(`/git/commits/${parentSha}`, token);
  const dateFolder = new Date().toISOString().slice(0, 10);
  const stamp = new Date().toISOString().replace(/[-:.TZ]/g, "");
  const treeEntries = [];
  const uploaded = [];

  for (let index = 0; index < files.length; index += 1) {
    const file = files[index];
    const uniqueName = `${stamp}-${String(index + 1).padStart(2, "0")}-${crypto.randomUUID().slice(0, 8)}-${safeName(file.name)}`;
    const path = `${photoFolder}/${dateFolder}/${uniqueName}`;
    const blob = await github("/git/blobs", token, {
      method: "POST",
      body: JSON.stringify({ content: bytesToBase64(new Uint8Array(await file.arrayBuffer())), encoding: "base64" }),
    });
    treeEntries.push({ path, mode: "100644", type: "blob", sha: blob.sha });
    uploaded.push({ path, name: uniqueName, size: file.size });
  }

  const tree = await github("/git/trees", token, {
    method: "POST",
    body: JSON.stringify({ base_tree: parentCommit.tree.sha, tree: treeEntries }),
  });
  const commit = await github("/git/commits", token, {
    method: "POST",
    body: JSON.stringify({
      message: `Add ${files.length} trip photo${files.length === 1 ? "" : "s"}`,
      tree: tree.sha,
      parents: [parentSha],
      author: { name: "Japan 2026 Album", email },
    }),
  });
  await github(`/git/refs/heads/${encodeURIComponent(branch)}`, token, {
    method: "PATCH",
    body: JSON.stringify({ sha: commit.sha, force: false }),
  });
  return json({ uploaded, commit: commit.sha }, 201);
}

async function deletePhoto(request: Request, token: string) {
  const body = await request.json();
  const path = String(body?.path || "");
  const sha = String(body?.sha || "");
  if (!path.startsWith(`${photoFolder}/`) || path.includes("..") || !sha) return json({ error: "Invalid photo path" }, 400);
  await github(`/contents/${path.split("/").map(encodeURIComponent).join("/")}`, token, {
    method: "DELETE",
    body: JSON.stringify({ message: `Remove trip photo ${path.split("/").pop()}`, sha, branch }),
  });
  return json({ deleted: path });
}

Deno.serve(async request => {
  if (request.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  const githubToken = Deno.env.get("GITHUB_TOKEN")?.replace(/\s/g, "").replace(/^["']|["']$/g, "");
  if (!githubToken || !/^(?:github_pat_|ghp_)[A-Za-z0-9_-]{20,}$/.test(githubToken)) {
    return json({ error: "Photo repository token is invalid" }, 503);
  }

  const authorization = request.headers.get("Authorization") || "";
  const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY") || "";
  const authResponse = await fetch(`${supabaseUrl}/auth/v1/user`, {
    headers: { Authorization: authorization, apikey: anonKey },
  });
  if (!authResponse.ok) return json({ error: "Authentication required" }, 401);
  const user = await authResponse.json();

  try {
    if (request.method === "GET") return json({ photos: await listPhotos(githubToken) });
    if (request.method === "POST") return await uploadPhotos(request, githubToken, String(user.email || "trip-album@users.noreply.github.com"));
    if (request.method === "DELETE") return await deletePhoto(request, githubToken);
    return json({ error: "Method not allowed" }, 405);
  } catch (error) {
    console.error(error);
    return json({ error: error instanceof Error ? error.message : "Unexpected server error" }, 502);
  }
});
