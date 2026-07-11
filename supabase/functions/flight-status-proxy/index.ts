import "@supabase/functions-js/edge-runtime.d.ts";
import { withSupabase } from "@supabase/server";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function mapStatus(status: string | null | undefined): "on-time" | "delayed" | "unknown" {
  const value = String(status || "").toLowerCase();
  if (value === "delayed" || value === "cancelled" || value === "diverted") return "delayed";
  if (value === "scheduled" || value === "active" || value === "landed") return "on-time";
  return "unknown";
}

export default {
  fetch: withSupabase({ auth: ["publishable", "secret"] }, async (req) => {
    if (req.method === "OPTIONS") {
      return new Response("ok", { headers: corsHeaders });
    }

    if (req.method !== "POST") {
      return new Response(JSON.stringify({ error: "Method not allowed" }), {
        status: 405,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const apiKey = Deno.env.get("AVIATIONSTACK_API_KEY");
    if (!apiKey) {
      return new Response(JSON.stringify({ error: "Missing server API key" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    let flight = "";
    try {
      const body = await req.json();
      flight = String(body?.flight || "").trim().toUpperCase();
    } catch {
      return new Response(JSON.stringify({ error: "Invalid JSON body" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    if (!flight) {
      return new Response(JSON.stringify({ error: "flight is required" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const url = `https://api.aviationstack.com/v1/flights?access_key=${encodeURIComponent(apiKey)}&flight_iata=${encodeURIComponent(flight)}&limit=1`;
    const response = await fetch(url, { method: "GET" });
    if (!response.ok) {
      return new Response(JSON.stringify({ error: `Aviationstack HTTP ${response.status}` }), {
        status: 502,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const payload = await response.json();
    const row = payload?.data?.[0];
    if (!row) {
      return new Response(JSON.stringify({ error: `No data for ${flight}` }), {
        status: 404,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const gate = row?.departure?.gate || row?.arrival?.gate || "";
    const data = {
      flight,
      status: mapStatus(row?.flight_status),
      gate: String(gate || "").trim(),
      sourceStatus: String(row?.flight_status || ""),
      updatedAt: new Date().toISOString(),
    };

    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }),
};
