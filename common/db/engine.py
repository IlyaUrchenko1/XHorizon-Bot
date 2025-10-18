from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from settings.config import config


def create_engine() -> AsyncEngine:
    return create_async_engine(
        config.SQLALCHEMY_DATABASE_URI,
        echo=config.DB_ECHO,
        pool_size=config.DB_POOL_SIZE,
        max_overflow=config.DB_MAX_OVERFLOW,
        pool_timeout=config.DB_POOL_TIMEOUT,
        future=True,
    )


async_engine: AsyncEngine = create_engine()
