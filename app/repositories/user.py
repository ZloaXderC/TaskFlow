from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserORM
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class UserRepository:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def create(self, email: str, hashed_password : str):
        new_user = UserORM(
            email=email,
            hashed_password = hashed_password
            )
        
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def get_by_email(self, email: str):
        stmt = select(UserORM).where(UserORM.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def get_by_id(self, user_id: UUID):
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def get_user_with_tasks(self, user_id: UUID):
        stmt = select(UserORM).where(UserORM.id == user_id).options(selectinload(UserORM.tasks))
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        return user



