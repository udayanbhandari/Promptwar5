"""Main FastAPI application entry point with middleware, routing, and error handlers."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.security import SecurityHeadersMiddleware, limiter
from app.db.session import Base, engine
from app.routers.events import router as events_router
from app.routers.plan import router as plan_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: reset the SQLite schema on startup for reliable local dev parity."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="EventPilot: GenAI-powered Celebration & Event Planner Backend",
    lifespan=lifespan,
)

# Connect slowapi rate limiter to app state
app.state.limiter = limiter

# -----------------------------------------------------------------------------
# Middleware Configuration
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)
app.add_middleware(SecurityHeadersMiddleware)


# -----------------------------------------------------------------------------
# Standardized Error Handlers
# -----------------------------------------------------------------------------
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Format rate limit violations consistently."""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "rate_limit_exceeded",
            "message": "Too many requests. Please slow down and try again shortly.",
            "details": None,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Format request validation errors consistently."""
    details = []
    for err in exc.errors():
        field_path = " -> ".join(str(loc) for loc in err.get("loc", []))
        details.append(
            {
                "field": field_path,
                "issue": err.get("msg", "Invalid value"),
                "type": err.get("type", "value_error"),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "message": "Input validation failed. Please check the provided fields.",
            "details": details,
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Format standard HTTP exceptions consistently."""
    error_code = "http_error"
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        error_code = "not_found"
    elif exc.status_code == status.HTTP_400_BAD_REQUEST:
        error_code = "bad_request"
    elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
        error_code = "unauthorized"
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        error_code = "forbidden"

    message = exc.detail if isinstance(exc.detail, str) else "An HTTP error occurred"
    details = exc.detail if not isinstance(exc.detail, str) else None

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": error_code,
            "message": message,
            "details": details,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all unhandled server error handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "An unexpected server error occurred.",
            "details": None,
        },
    )


# -----------------------------------------------------------------------------
# Base Endpoints
# -----------------------------------------------------------------------------
@app.get("/health", tags=["System"], summary="Health check endpoint")
def health_check() -> dict:
    """Return health status and API version."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


# -----------------------------------------------------------------------------
# Versioned API Routers
# -----------------------------------------------------------------------------
app.include_router(events_router, prefix=settings.API_V1_STR)
app.include_router(plan_router, prefix=settings.API_V1_STR)
