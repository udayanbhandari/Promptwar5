# Quality after

Measured after the refactoring pass. Backend tests remained at 66 passing and
frontend tests remained at 4 files / 4 tests passing.

## Metrics

| Metric | Before | After | Result |
| --- | ---: | ---: | --- |
| Radon average cyclomatic complexity | 3.56 (A) | 3.16 (A) | Improved |
| Highest measured complexity | E / 37 | C / 15 | Improved |
| Lowest maintainability index | B, above 70 | A | Improved |
| Python source files over 300 lines | 4 | 0 | Fixed |
| jscpd duplicated lines | 141 (2.60%) | 104 (1.96%) | Improved |
| jscpd clone groups | 12 | 8 | Improved |
| Frontend metric errors | 6 | 0 | Fixed |
| Frontend metric warnings | 54 | 48 | Improved |
| Strict mypy errors | 27 | 29 | Open; new service/module boundaries exposed additional typing gaps |
| Backend tests | 66 passed | 66 passed | Preserved |
| Frontend tests | 4 files / 4 passed | 4 files / 4 passed | Preserved |
| Frontend TypeScript check | Passed | Passed | Preserved |

## Files split or created

- Split fallback registries into `budget_fallbacks.py`, `idea_fallbacks.py`,
  `risk_fallbacks.py`, and `vendor_fallbacks.py`.
- Moved plan orchestration into `services/plan_service.py`.
- Split timeline templates into event-specific wedding, birthday, and community
  modules.
- Split dashboard rendering into focused tab components and
  `DashboardLayout.tsx`.
- Split wizard step rendering into `WizardSteps.tsx` subcomponents.
- Added `.pre-commit-config.yaml` and CI complexity, file-size, and duplication
  gates.

## Intentionally left

- Strict mypy still needs a dedicated typing pass for SQLAlchemy models,
  middleware/lifespan signatures, generic dictionaries, and untyped Google
  GenAI dependencies.
- Frontend `no-magic-numbers` warnings remain in existing display and date
  calculations; they do not affect runtime behavior and should be addressed by
  a shared constants pass.
- The duplication threshold is below the requested 3% CI ceiling, but the
  remaining repeated Pydantic validators and model declarations are candidates
  for a future shared-helper extraction.
