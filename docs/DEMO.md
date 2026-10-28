# Demo script

This is a short product walkthrough for the current EventPilot prototype. It is designed to fit in roughly 3 minutes while showing the main value: guide the user, generate a resilient plan, and recover gracefully when AI is unavailable.

## 1) Setup (20 seconds)

1. Start the backend:
   `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
2. Start the frontend:
   `cd frontend && npm run dev -- --host 0.0.0.0 --port 5173`
3. Open the app at `http://localhost:5173`.

## 2) Wedding event flow (45 seconds)

1. In the wizard, choose `Wedding`.
2. Set a future date and guest count such as 120 guests.
3. Enter a budget such as `$28,000` and a city such as `Seattle, WA`.
4. Add a theme like `Warm Minimalist` and must-haves such as `vegetarian options` and `wheelchair access`.
5. Complete the wizard and click the final action to create the event.
6. The app posts the event and immediately calls the plan-generation endpoint.
7. The plan page shows generated categories, recommended idea cards, and tasks produced by the budget and timeline engines.

## 3) Deliberate AI failure (30 seconds)

1. Stop the Gemini API key from being configured by leaving `GEMINI_API_KEY` empty in the backend env.
2. Trigger `generate-plan` again.
3. The app should no longer call the remote model and instead use the deterministic fallback templates in `backend/app/services/fallbacks.py`.
4. The UI should show a gentle fallback state or process as a normal generated plan; the budget and ideas still remain valid and consistent.

This deliberate failure demonstrates the fallback mode without breaking the product.

## 4) Birthday event flow (40 seconds)

1. Create a second event as a birthday.
2. Choose a smaller budget and a more energetic theme such as `Retro Neon Arcade`.
3. Generate the plan.
4. Review how the system adapts the category mix, task scheduling, and idea cards to the event type.
5. Check how the generated budget remains exact and the timeline remains realistic for a short lead time.

## 5) Community event flow (40 seconds)

1. Create a third event as a community event.
2. Pick a higher attendance count, a city, and requirements such as accessibility and public-safety needs.
3. Generate the plan.
4. Highlight how the budget emphasizes permits, equipment, signage, and safety, and how the task timeline reflects operational dependencies.

## 6) Plan B simulation (30 seconds)

1. Open the Plan B page in the frontend mock flow or run the risk simulation path in the backend service layer.
2. Select a scenario such as `weather disruption` or `guest surge`.
3. Run the simulation to compare the before and after budget totals.
4. Confirm that the tool shows affected tasks and mitigation/fallback steps.

This demonstrates the contingency logic without requiring a live AI call.

## 7) Closing message (15 seconds)

Emphasize the core promise of the product: the AI proposes creative guidance, but the code verifies math, schedules, and structure before the plan is trusted.
