from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


engine = create_async_engine(settings.DATABASE_URL)
session_factory = async_sessionmaker(engine)

async def get_db():
    async with session_factory() as session:
        yield session





