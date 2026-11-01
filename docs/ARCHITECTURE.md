# Architecture

EventPilot uses a layered FastAPI backend and a React frontend.

```mermaid
flowchart LR
    UI[React + Vite frontend] --> R[FastAPI routers]
    R --> S[AI and domain services]
    S --> E[Deterministic engines]
    E --> M[SQLAlchemy models]
    M --> DB[(SQLite in development)]
    S --> AI[Google GenAI]
    S --> F[Fallback templates]
```

## Layers

- **Frontend**: `frontend/src` contains the wizard, dashboard, Plan B, run
  sheet, and shared-view pages. API calls are centralized in the client.
- **Routers**: `backend/app/routers` validates HTTP input, coordinates
  services/engines, and serializes responses.
- **Services**: `backend/app/services` owns AI calls, schema validation, and
  deterministic fallback selection.
- **Engines**: `backend/app/engines` contains pure budget, timeline, and run
  sheet calculations. Engines do not call the LLM or database.
- **Models and database**: `backend/app/models` and `backend/app/db` persist
  events and generated plan records through SQLAlchemy.
- **Schemas and prompts**: `backend/app/schemas` defines API and AI contracts;
  `backend/app/prompts` contains versioned prompt builders.

## Plan data flow

1. The frontend submits an event to the events API.
2. The plan router requests structured AI suggestions when a Gemini key is
   configured.
3. Invalid or unavailable AI output uses the matching deterministic fallback.
4. Budget and timeline engines normalize the suggestions into exact,
   dependency-ordered records.
5. The router persists the generated records and returns the plan payload.
