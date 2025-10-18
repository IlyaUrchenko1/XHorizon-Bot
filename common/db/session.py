from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from common.db.engine import async_engine


async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
