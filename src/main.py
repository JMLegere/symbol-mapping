"""Application entry point."""

from fastapi import FastAPI

from .routers.mapping import router as mapping_router


def create_app() -> FastAPI:
    """Construct and configure the FastAPI application."""

    application = FastAPI()
    application.include_router(mapping_router)
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
