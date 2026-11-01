# Security

EventPilot is a local-development prototype. The controls below describe the
implemented behavior; production deployment still requires managed secrets,
HTTPS, a persistent database, and an authenticated identity provider.

| Threat | Mitigation | File | Test/evidence |
| --- | --- | --- | --- |
| Cross-origin requests | Configured origin, method, and header allow-lists | `backend/app/main.py`, `backend/app/core/config.py` | CORS preflight tests in `backend/tests` |
| Missing browser security headers | CSP, frame, MIME, referrer, permissions, and HSTS headers | `backend/app/core/security.py` | Response middleware behavior |
| Oversized or malformed input | Pydantic request schemas and bounded string fields | `backend/app/schemas/` | `backend/tests/test_validation_edge_cases.py` |
| Prompt injection or unsafe model output | Delimited, normalized prompt input and schema validation with deterministic fallback | `backend/app/services/ai_client.py` | `backend/tests/test_ai_client.py` |
| Brute-force API use | SlowAPI default and AI-specific limits | `backend/app/core/security.py`, `backend/app/routers/` | Rate-limit tests |
| Secret leakage in logs | Metadata-only AI logging and redaction helper | `backend/app/services/ai_client.py`, `backend/app/core/security.py` | Code review and client tests |
| SQL injection | SQLAlchemy ORM and validated schemas; no raw SQL query construction | `backend/app/db/`, `backend/app/routers/` | CRUD and validation tests |
| Error information disclosure | Generic global exception response without exception details | `backend/app/main.py` | Error-handler behavior |

## Responsible AI

AI output is advisory. Pydantic schemas validate generated structures, while
budget and timeline engines enforce deterministic arithmetic and dependency
rules. If Gemini is unavailable, the application uses deterministic templates
instead of blocking plan creation. Users should review vendor, safety, legal,
accessibility, and financial decisions before acting on a generated plan.
