"""Gemini AI client with structured outputs, prompt-injection defense, and retries."""

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from typing import TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

from app.core.config import get_settings
from app.services.errors import AIError, AIUnavailable

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

MAX_PROMPT_LENGTH = 10000
MAX_OUTPUT_TOKENS = 4096
DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_RETRIES = 2


def wrap_user_input(text: str | None) -> str:
    """Enclose user input inside strict XML delimiters to neutralize prompt injection.

    Instructs downstream prompts to interpret everything inside delimiters as
    pure data rather than executive instructions.
    """
    if not text:
        return "<user_data></user_data>"
    # Neutralize attempts to close or manipulate delimiter boundaries
    sanitized = text.replace("</user_data>", "").replace("<user_data>", "")
    return f"<user_data>\n{sanitized.strip()}\n</user_data>"


def generate_structured(
    prompt: str,
    schema: type[T],
    client: genai.Client | None = None,
    max_retries: int = MAX_RETRIES,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> T:
    """Generate structured JSON output from Gemini and validate against a Pydantic schema.

    - Validates GEMINI_API_KEY existence upfront; raises AIUnavailable immediately if missing.
    - Limits prompt length to prevent resource exhaustion.
    - Configures Gemini in JSON schema enforcement mode.
    - Retries on malformed JSON or validation errors, feeding the error back to the model.
    - Enforces a per-call timeout and uses exponential backoff between retries.
    - Logs metadata (timing, attempts, success), never logging user data or prompt contents.
    """
    settings = get_settings()

    if not settings.GEMINI_API_KEY:
        logger.warning(
            "AI request skipped: GEMINI_API_KEY not configured.",
            extra={"schema": schema.__name__, "success": False},
        )
        raise AIUnavailable("GEMINI_API_KEY is not configured.")

    if len(prompt) > MAX_PROMPT_LENGTH:
        raise AIError(f"Prompt length {len(prompt)} exceeds maximum limit of {MAX_PROMPT_LENGTH}.")

    # Initialize client if not injected for testing
    if client is None:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

    model_name = settings.GEMINI_MODEL or "gemini-2.5-flash"
    schema_name = schema.__name__

    current_prompt = prompt
    last_error: Exception | None = None

    for attempt in range(max_retries + 1):
        start_time = time.perf_counter()
        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                temperature=0.2,
            )

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    client.models.generate_content,
                    model=model_name,
                    contents=current_prompt,
                    config=config,
                )
                response = future.result(timeout=timeout)

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            raw_text = getattr(response, "text", "") or ""
            if not raw_text.strip():
                raise ValueError("Model returned an empty text response.")

            # Validate against Pydantic schema
            parsed_data = schema.model_validate_json(raw_text)

            logger.info(
                "AI generation succeeded",
                extra={
                    "latency_ms": latency_ms,
                    "attempt": attempt + 1,
                    "schema": schema_name,
                    "model": model_name,
                    "success": True,
                },
            )
            return parsed_data

        except (FutureTimeoutError, TimeoutError, ValidationError, ValueError, json.JSONDecodeError) as parse_err:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            last_error = parse_err
            logger.warning(
                "AI output validation failed, retrying...",
                extra={
                    "latency_ms": latency_ms,
                    "attempt": attempt + 1,
                    "schema": schema_name,
                    "model": model_name,
                    "error_type": type(parse_err).__name__,
                    "success": False,
                },
            )

            if attempt < max_retries:
                # Exponential backoff
                time.sleep(0.5 * (2**attempt))
                # Feed error back to model for correction
                error_feedback = (
                    f"\n\n[CORRECTION REQUIRED: Your previous response was invalid. "
                    f"Error: {str(parse_err)}. "
                    f"Return ONLY valid JSON that strictly satisfies the required schema.]"
                )
                current_prompt = prompt + error_feedback

        except Exception as api_err:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            last_error = api_err
            logger.error(
                "AI service API call failed",
                extra={
                    "latency_ms": latency_ms,
                    "attempt": attempt + 1,
                    "schema": schema_name,
                    "model": model_name,
                    "error_type": type(api_err).__name__,
                    "success": False,
                },
            )
            if attempt < max_retries:
                time.sleep(0.5 * (2**attempt))

    # All retries exhausted
    raise AIUnavailable(f"AI service unavailable after {max_retries + 1} attempts. Root cause: {last_error}")
