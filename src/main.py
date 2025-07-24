from fastapi import FastAPI

from .routers.mapping import router as mapping_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(mapping_router)
    return app


app = create_app()


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
