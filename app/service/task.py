from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import TaskCreate, TaskUpdate
from app.repositories.task import TaskRepository


class TaskService:
    def __init__(self, db: AsyncSession):
        repository = TaskRepository(db)
        self.repository = repository

    async def create(self, task_data: TaskCreate, user_id: UUID):
        created_task = await self.repository.create(task_data.title, user_id)
        return created_task

    async def get_tasks(
            self,
            user_id: UUID,
            limit: int,
            offset: int,
            complited: bool | None,
            sort: str | None,
            search: str | None
            ):
        
        return await self.repository.get_tasks(user_id, limit, offset, complited, sort, search)

    async def get_by_id(
            self,
            task_id: UUID,
            user_id: UUID
    ):
        task = await self.repository.get_by_id(task_id, user_id)

        if task is None:
            raise ValueError("Task not found")
        
        return task

    async def update(
            self,
            task_id: UUID,
            user_id: UUID,
            task_data: TaskUpdate,
            current_user
    ):
        
        task = await self.repository.get_by_id(task_id,user_id) 
       

        if not task:
            raise ValueError("Task not found")
        
        if task.user_id != current_user.id:
            raise ValueError("Access denied")

        task = await self.repository.update(task_id,user_id,task_data)
        
        return task

    async def delete(
            self,
            task_id: UUID,
            user_id: UUID
    ):
        task = await self.repository.delete(task_id,user_id)

        if task is None:
            raise ValueError("Task not found")

        return task
        