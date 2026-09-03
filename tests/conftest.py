from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.main import app
from app.db.database import get_db
from app.db.base import Base

from app.models.user import UserORM
from app.models.task import TaskORM
from sqlalchemy import delete
from sqlalchemy.pool import NullPool

from httpx import AsyncClient, ASGITransport

import pytest_asyncio

test_engine = create_async_engine(settings.TEST_DATABASE_URL, poolclass = NullPool)

test_session_factory = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def override_get_db():
    async with test_session_factory() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 
        await conn.run_sync(Base.metadata.create_all) 

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app) 
    async with AsyncClient(transport=transport, base_url="https://test") as client:
        yield client

# @pytest_asyncio.fixture(autouse= True)
# async def clean_database():
#     async with test_session_factory() as session:
#         await session.execute(delete(TaskORM))
#         await session.execute(delete(UserORM))
#         await session.commit()