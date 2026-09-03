from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import TaskORM
from sqlalchemy import select

from app.schemas.task import TaskUpdate

from sqlalchemy.orm import selectinload


class TaskRepository:
    def __init__ (self, db: AsyncSession):
        self.db = db

    async def create(self, title: str, user_id: UUID):
        new_task = TaskORM(
            title = title,
            user_id = user_id
            )

        self.db.add(new_task)

        try:
            await self.db.commit()
            
        except Exception:
            await self.db.rollback()
            raise 

        await self.db.refresh(new_task)
        
        return new_task
    
    async def get_tasks(
            self,
            user_id: UUID,
            limit:int,
            offset: int,
            complited: bool | None,
            sort: str | None,
            search: str| None
            ):
        
        stmt = select(TaskORM).where(TaskORM.user_id == user_id)

        if complited is not None:
            stmt = stmt.where(TaskORM.complited == complited)

        if search is not None:
            stmt = stmt.where(TaskORM.title.ilike(f"%{search}%"))

        if sort == "title":
            stmt = stmt.order_by(TaskORM.title.asc())

        elif sort == "-title":
            stmt = stmt.order_by(TaskORM.title.desc())

        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        tasks = result.scalars().all()

        return tasks

    async def get_by_id(
            self,
            task_id: UUID,
            user_id: UUID
    ):
        
        stmt = select(TaskORM).where(
            TaskORM.id == task_id,
            TaskORM.user_id == user_id)
        
        result = await self.db.execute(stmt)
        tasks = result.scalar_one_or_none()

        return tasks

    async def update(
            self,
            task_id: UUID,
            user_id: UUID,
            task_data: TaskUpdate
            ):
        
        task = await self.get_by_id(task_id,user_id)

        if not task:
            return None

        if task_data.title is not None:
            task.title = task_data.title 

        if task_data.complited is not None:
            task.complited = task_data.complited

        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

        await self.db.refresh(task)
        return task

    async def delete(
            self,
            task_id: UUID,
            user_id: UUID,    
    ):
        task = await self.get_by_id(task_id,user_id)

        if not task: 
            return None

        await self.db.delete(task)

        try:
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

        return task

    async def get_task_with_user(self, task_id: UUID, user_id: UUID):
        stmt = select(TaskORM).where(
            TaskORM.id == task_id,
            TaskORM.user_id == user_id
        ).options(
            selectinload(TaskORM.user)
        )

        result = await self.db.execute(stmt)
        task = result.scalar_one_or_none()

        return task
    
