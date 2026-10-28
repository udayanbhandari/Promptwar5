# Project requirement checklist

This checklist reflects the repository as it exists in the current workspace and does not claim features that are not implemented in code.

| Requirement | Status | Notes |
| --- | --- | --- |
| GenAI-powered planning assistant | PASS | The backend uses a Google GenAI client, structured schemas, and prompt templates to generate event-planning suggestions. |
| Wedding, birthday, and community event support | PASS | Event type enums and prompt logic cover these three event categories. |
| AI proposal + deterministic verification | PASS | AI output is validated and then verified by Python budget/timeline engines. |
| Structured prompt versioning | PASS | Prompt files use `*_v1` naming and export a version constant. |
| Prompt-injection defense | PASS | `wrap_user_input()` places user text inside `<user_data>` delimiters. |
| Retry and validation loop | PASS | The AI client retries malformed/invalid JSON up to two times and then raises `AIUnavailable`. |
| Fallback without API key | PASS | Missing `GEMINI_API_KEY` triggers the fallback path and deterministic templates. |
| Budget split generation | PASS | `backend/app/prompts/budget_split_v1.py` and `backend/app/engines/budget_engine.py` implement it. |
| Timeline generation | PASS | `backend/app/engines/timeline_engine.py` and the generated tasks in the plan router produce a task schedule. |
| Vendor category generation | PASS | The vendor-category prompt and schema are implemented. |
| Event CRUD API | PASS | `backend/app/routers/events.py` provides create/list/detail/update/delete operations. |
| Plan-generation endpoint | PASS | `POST /api/v1/events/{event_id}/generate-plan` is implemented and tested. |
| Plan retrieval endpoint | PASS | `GET /api/v1/events/{event_id}/plan` is implemented. |
| Notable security hardening | PASS | Input sanitization, rate limiting, allow-listed CORS, and environment-based settings are present. |
| Frontend wizard and dashboard navigation | PASS | React pages for the wizard and dashboard exist and run in tests. |
| Frontend production build | PASS | `npm run build` succeeds. |
| Frontend test suite | PASS | Vitest tests pass. |
| Backend test suite | PASS | `pytest` passes in the current workspace. |
| Docker compose configuration | PASS | Docker Compose exists with a backend service and persisted volume. |
| Public share-link endpoint family | FAIL | No backend `share` router exists in the committed code. |
| Vendor brief and vendor management API | FAIL | No backend vendor router or public `/vendors` route exists in the committed code. |
| Full Plan B backend route family | PARTIAL | The risk service exists, but the public `/events/{id}/risks` endpoints are not present in the committed router tree. |
| Complete end-to-end advanced feature parity with the challenge statement | FAIL | The codebase supports the core plan-generation flow but does not expose the full advanced feature set described in the challenge text. |

## Verification status

The project is in a sound working state for the implemented feature set, but it does not currently cover the full advanced challenge surface area described in the larger narrative. The current README intentionally reflects only the code that is present and verified in this workspace.
