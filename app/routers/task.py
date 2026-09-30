from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.dependecies.auth import get_current_user
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.service.task import TaskService
from app.schemas.task import TaskResponse


router = APIRouter(prefix="/task", tags= ["Task"])

@router.post("", response_model = TaskResponse, status_code= status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
    ):

    service = TaskService(db)
    
    return await service.create(task_data, current_user.id)

@router.get("", response_model= list[TaskResponse])
async def get_tasks(
    current_user = Depends(get_current_user),
    db : AsyncSession =Depends(get_db),
    limit: int = Query(default=20, ge=1, le =100),
    offset: int = Query(default=0, ge=0),
    complited: bool | None = None,
    sort: str | None = None,
    search: str | None = None
    ):

    service = TaskService(db)

    if search is not None:
        search = search.strip()

        if not search:
            search = None

    tasks = await service.get_tasks(current_user.id, limit, offset, complited,sort, search)
    return tasks

@router.get("/{task_id}", response_model= TaskResponse)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    
    ):

    service = TaskService(db)
    try:
        task = await service.get_by_id(
            task_id,
            current_user.id
            )
        return task

    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
     
@router.patch("/{task_id}", response_model=TaskResponse)
async def update(
    task_id: UUID,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)  
):
    print("UPDATE ROUTER CALLED")
    service = TaskService(db)

    try:
        task = await service.update(
            task_id = task_id,
            user_id=current_user.id,
            task_data = task_data,
            current_user = current_user
            
        )
        return task
    
    except ValueError as error:
        if str(error) == "Access denied":
            raise HTTPException(status_code = 403, detail = str(error))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.delete("/{task_id}", response_model=TaskResponse)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    service = TaskService(db)

    try:
        task = await service.delete(
            task_id,
            current_user.id
        )
        return task
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    






