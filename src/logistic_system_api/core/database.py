from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.logistic_system_api.core.settings import Settings

settings = Settings()

engine = create_async_engine(
    settings.DATABASE_URL, pool_size=5, max_overflow=0, pool_pre_ping=True
)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def close_engine():
    await engine.dispose()
