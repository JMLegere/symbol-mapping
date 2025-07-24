"""Application entry point."""

from fastapi import FastAPI

from .routers.enrichment import router as enrichment_router
from .utils.ratelimit_middleware import RateLimitMiddleware


def create_app(max_requests: int = 60, window_seconds: int = 60) -> FastAPI:
    """Construct and configure the FastAPI application."""

    application = FastAPI()
    application.add_middleware(
        RateLimitMiddleware,
        max_requests=max_requests,
        window_seconds=window_seconds,
    )
    application.include_router(enrichment_router)
    return application


app = create_app()


def main() -> None:  # pragma: no cover - manual start
    """Run the application with uvicorn."""

    import os
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
