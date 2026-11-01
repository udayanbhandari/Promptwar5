# Quality baseline

Measured before refactoring on 2026-11-01. The backend and frontend test suites
passed before measurement: backend `66 passed`; frontend `4 test files, 4
tests passed`.

## Commands and raw results

### Backend complexity and maintainability

```text
$ radon cc -s -a backend/app
139 blocks (classes, functions, methods) analyzed.
Average complexity: A (3.5611510791366907)

Highest-complexity blocks:
app/engines/budget_engine.py: recalculate - E (37)
app/engines/budget_engine.py: allocate - C (20)
app/engines/budget_engine.py: warnings - C (20)
app/routers/plan.py: generate_plan - C (19)
app/engines/timeline_engine.py: build_timeline - C (16)
app/core/config.py: Settings.assemble_origins - C (15)
app/engines/timeline_engine.py: _topological_order - C (14)
app/services/risk_service.py: _scenario_type_for - C (14)
app/services/ai_client.py: generate_structured - C (12)
app/engines/budget_engine.py: _coerce_item_dicts - C (12)

$ radon mi backend/app
Files ranged from A through B. The only B-rated backend file was
backend/app/engines/budget_engine.py; no file was below MI 70.
```

### Ruff

```text
$ ruff check --select C901,PLR0912,PLR0913,PLR0915,B,SIM,N,D backend
Targeted findings included:
- D102: SecurityHeadersMiddleware.dispatch missing docstring
- C901/PLR0912/PLR0915: budget_engine.recalculate
- C901: budget_engine.allocate
- PLR0913: prompts/vendor_brief_v1.build_prompt
- D401: routers/events.update_event
- D102: AI output validator methods
The command exited non-zero.
```

### Strict mypy

```text
$ mypy --strict backend/app
Found 27 errors in 15 files (checked 45 source files)

Main categories:
- missing type parameters for dict in engines/templates.py,
  engines/timeline_engine.py, and engines/runsheet_engine.py
- untyped middleware/route/lifespan functions
- untyped SQLAlchemy Base inheritance in model modules
- missing third-party google stubs
- AIUnavailable re-export errors
```

### Duplication

```text
$ npx jscpd backend/app frontend/src --min-lines 6
Found 12 clones.
Total: 57 files, 5432 lines, 12 clones, 141 duplicated lines,
2.60% duplicated lines, 787 duplicated tokens.

Clone groups:
- models/budget_item.py and models/vendor.py
- routers/plan.py internal helper blocks
- routers/plan.py and services/risk_service.py
- schemas/budget.py repeated validators
- schemas/budget.py, schemas/risk.py, schemas/task.py repeated validators
- schemas/event.py repeated sanitizers
- schemas/risk.py repeated validators
- schemas/task.py repeated validators
- schemas/vendor.py repeated sanitizers
```

### Frontend ESLint and TypeScript

```text
$ eslint . --complexity 10 --max-lines 300 --max-lines-per-function 60
6 errors and 54 warnings.

Errors:
- DashboardPage: 204 lines, complexity 21
- PlanBPage: 115 lines
- WizardPage: 327 lines, complexity 12
- Wizard.tsx: 369 lines

Warnings were primarily no-magic-numbers findings in ProgressBar, Skeleton,
Toast, Dashboard, PlanB, and Wizard.

$ tsc --noEmit --strict
Passed with no diagnostics.
```

## Size inventory

### Ten longest files

| Lines | File |
| ---: | --- |
| 545 | backend/app/services/fallbacks.py |
| 369 | frontend/src/pages/Wizard.tsx |
| 364 | backend/app/engines/templates.py |
| 303 | backend/app/routers/plan.py |
| 268 | backend/app/engines/budget_engine.py |
| 217 | frontend/src/pages/Dashboard.tsx |
| 198 | backend/app/engines/timeline_engine.py |
| 197 | frontend/src/types/index.ts |
| 162 | backend/app/services/ai_client.py |
| 146 | backend/app/main.py |

### Ten longest Python functions

| Lines | Function |
| ---: | --- |
| 135 | backend/app/routers/plan.py:generate_plan |
| 123 | backend/app/services/ai_client.py:generate_structured |
| 90 | backend/app/engines/budget_engine.py:recalculate |
| 49 | backend/app/routers/plan.py:get_plan |
| 49 | backend/app/engines/budget_engine.py:allocate |
| 42 | backend/app/prompts/ideas_v1.py:build_prompt |
| 41 | backend/app/prompts/budget_split_v1.py:build_prompt |
| 41 | backend/app/engines/timeline_engine.py:build_timeline |
| 39 | backend/app/routers/plan.py:_ai_plan_payload |
| 38 | backend/app/engines/budget_engine.py:warnings |

## Raw report locations

The complete command captures used to compile this report are retained in the
session workspace under `files/radon-baseline.txt`, `files/ruff-baseline.txt`,
`files/mypy-baseline.txt`, `files/jscpd-baseline.txt`, and
`files/frontend-baseline-correct.txt`.
