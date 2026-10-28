# Prompt reference

This project uses versioned prompt modules under `backend/app/prompts` and validates every AI response through the schemas in `backend/app/schemas/ai_outputs.py`.

## Prompt inventory

| Prompt module | Version | Schema | What it produces |
| --- | --- | --- | --- |
| `budget_split_v1` | `budget_split_v1` | `BudgetSplitOutput` | Category percentages that sum to 100% and a one-line reason for each category |
| `ideas_v1` | `ideas_v1` | `IdeasOutput` | Exactly 5 event ideas covering theme, decor, food, entertainment, and memorable touch |
| `vendor_categories_v1` | `vendor_categories_v1` | `VendorCategoriesOutput` | Required vendor categories with 5 questions and 3 red flags each |
| `risk_scenarios_v1` | `risk_scenarios_v1` | `RiskScenariosOutput` | Five likely risk scenarios for the specific event |
| `vendor_brief_v1` | `vendor_brief_v1` | `VendorBriefOutput` | A WhatsApp/email-ready enquiry message and quote comparison checklist |

## Prompt construction pattern

Each prompt module follows the same structure:

1. Export a `VERSION` constant.
2. Export a `OutputSchema` reference.
3. Expose `build_prompt(...)` that accepts event or vendor context.
4. Wrap untrusted user text with `wrap_user_input(...)` and place it inside `<user_data>` delimiters.
5. Tell the model to treat the content as passive data, never as an instruction.

The implementation is in `backend/app/services/ai_client.py`.

## Structured output and validation

The AI client enforces structured JSON responses with the Google GenAI SDK:

- `response_mime_type="application/json"`
- `response_schema=schema`
- `max_output_tokens=4096`
- `temperature=0.2`

The generated content is then validated via Pydantic. When Google returns malformed JSON, empty output, or a payload that violates the schema, the app retries up to two additional times. On each failed retry, it appends a correction message such as: "Your previous response was invalid. Return ONLY valid JSON that strictly satisfies the required schema."

The retry loop is intentionally strict and uses exponential backoff.

## Prompt-injection defense

User-supplied values are wrapped before the model sees them. The helper is:

- `wrap_user_input(text) -> <user_data>...</user_data>`

The code strips closing tags and additional delimiter abuse before finalizing the prompt, then instructs the model to ignore any commands appearing inside the user data and treat that text as raw information.

## Fallback behavior

When no Gemini API key is configured, or when the model keeps failing after validation and retry attempts, the app raises `AIUnavailable` and the application falls back to deterministic templates in `backend/app/services/fallbacks.py`.

This fallback layer is important because it keeps the product usable even in offline, misconfigured, or quota-limited environments.

## Versioning and maintainability

The prompt modules are intentionally versioned (`*_v1`) so schema and prompt changes can be isolated without breaking earlier prompt consumers. This makes it easier to update guidance while preserving previous behavior under a stable contract.

## Core schemas

The schema contracts are defined in `backend/app/schemas/ai_outputs.py` and are enforced for all structured AI responses.

### `BudgetSplitOutput`

- `categories: List[CategoryPercentage]`
- Each category includes `category`, `percentage`, and `reason`
- Validation enforces the total to be approximately 100%

### `IdeasOutput`

- Must contain exactly five ideas
- The aspects must be exactly: `theme`, `decor`, `food`, `entertainment`, `memorable_touch`

### `VendorCategoriesOutput`

- Each category must include exactly five screening questions and exactly three red flags

### `RiskScenariosOutput`

- Exactly five scenarios are required
- Each scenario includes likelihood, impact, warning sign, fallback steps, and budget-impact percent

### `VendorBriefOutput`

- A ready-to-send `enquiry_message`
- A `comparison_checklist` of practical buying criteria

## Current implementation status

The repository currently includes the prompt modules, structured-output schemas, and fallback templates needed for the AI-assisted planning flow. The app remains resilient when Gemini is unavailable, and the code validates every AI payload before it is used in the plan-generation path.
