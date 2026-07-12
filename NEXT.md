# Japan 2026 - Next Steps

## Resume prompt to paste in Copilot Chat
Resume this project from latest checkpoint. Read PROGRESS.md and NEXT.md, summarize current state in 5 bullets, then continue from NEXT.md item 1.

## Next tasks
1. Verify Supabase secret AVIATIONSTACK_API_KEY is set in project ciabjdoqgedpszxngozu.
2. Open Transportation tab and run one manual sync to confirm live fields update.
3. Validate first day (12-13) and last day (28) Route pages show full original + live flight info.
4. Optional UI cleanup: reduce duplicated text lines in flight event descriptions for mobile readability.
5. Optional reliability improvement: add small backend health indicator in Transportation tab.

## Quick runbook
- Open project folder in VS Code: OneDrive - Intel Corporation/VSCode/japan2026
- Pull latest master
- If needed, redeploy function:
  - supabase functions deploy flight-status-proxy --no-verify-jwt
- App URL:
  - https://gilshenkar76.github.io/japan2026/index.html
