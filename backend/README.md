# EventPilot — Backend API

FastAPI backend foundation for EventPilot, built for PromptWars Challenge 5.

## Architecture

- **`app/main.py`**: FastAPI entrypoint with CORS, slowapi rate limiting, standardized JSON error envelopes, and `/health`.
- **`app/core/config.py`**: Settings management using Pydantic Settings.
- **`app/core/security.py`**: SlowAPI rate limiter and input sanitization helpers.
- **`app/db/session.py`**: SQLAlchemy engine, session maker, and `get_db` generator.
- **`app/db/models.py`**: SQLAlchemy ORM models (`Event`, `BudgetItem`, `Task`, `Vendor`, `RiskScenario`, `ShareLink`).
- **`app/schemas/`**: Pydantic v2 validation models with strict checks on guest count, future dates, positive budgets, and allow-listed currencies.
- **`app/routers/events.py`**: Versioned CRUD endpoints (`/api/v1/events`).
- **`tests/`**: Pytest test suite covering full CRUD lifecycles and validation edge cases.

## Running Locally

```bash
cd backend
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Running Tests

```bash
cd backend
pytest -v
```
