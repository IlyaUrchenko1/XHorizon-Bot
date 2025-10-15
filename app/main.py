import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.metrics import setup_instrumentator
from app.api.v1.endpoints.health import router as health_router

def create_app() -> FastAPI:
    setup_logging(settings.log_level)
    app = FastAPI()
    app.include_router(health_router)

    setup_instrumentator(app)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
