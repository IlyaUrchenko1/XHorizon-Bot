import uvicorn
from fastapi import FastAPI
from settings.config import config
from settings.logging_config import setup_logging
from app.api.v1.endpoints.health import router as health_router
from prometheus_fastapi_instrumentator import Instrumentator


def create_app() -> FastAPI:
    setup_logging(config.LOG_LEVEL)
    app = FastAPI()
    app.include_router(health_router)

    Instrumentator().instrument(app).expose(app)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=config.HOST, port=config.PORT, reload=True)
