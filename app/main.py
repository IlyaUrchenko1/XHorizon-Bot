import uvicorn
from fastapi import FastAPI
from settings.config import config
from settings.logging_config import setup_logging
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.users import router as users_router, ranks_router
from app.api.v1.endpoints.finance import currencies as currencies_router, wallets as wallets_router, transactions as transactions_router
from app.api.v1.endpoints.referrals import router as referrals_router, rewards as rewards_router
from app.api.v1.endpoints.auth import router as auth_router
from prometheus_fastapi_instrumentator import Instrumentator


def create_app() -> FastAPI:
    setup_logging(config.LOG_LEVEL)
    app = FastAPI()
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(ranks_router)
    app.include_router(currencies_router)
    app.include_router(wallets_router)
    app.include_router(transactions_router)
    app.include_router(referrals_router)
    app.include_router(rewards_router)

    Instrumentator().instrument(app).expose(app)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=config.HOST, port=config.PORT, reload=True)
