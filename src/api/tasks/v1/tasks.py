import uuid

from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep
from src.api.user.v1.dependencies.jwt_dependencies import get_current_account
from src.schemas.response import ResponseCreateNewTask
from src.schemas.response.task.delete import ResponseDeleteTask
from src.schemas.task import CreateTaskSchema, TaskSchema
from src.schemas.task.task import DeleteTaskSchema, ChangeTaskSchema
from src.schemas.user import AccountSchema
from src.servises.task import TaskService

router = APIRouter(prefix="/task/v1", tags=["Tasks operations"])


@router.post("/", response_model=ResponseCreateNewTask)
async def create_task(uow: UOWDep, task: CreateTaskSchema, account: AccountSchema = Depends(get_current_account)):
    task: TaskSchema = await TaskService().create_task(uow, task, account)
    return ResponseCreateNewTask(
        status=201,
        error=False,
        payload=task,
        detail="The task successfully created",
    )


@router.delete("/{task_id}", response_model=ResponseDeleteTask)
async def delete_task(uow: UOWDep, task_id: uuid.UUID, account: AccountSchema = Depends(get_current_account)):
    task: DeleteTaskSchema = await TaskService().delete_task(uow, task_id)
    return ResponseDeleteTask(
        status=204,
        error=False,
        payload=task,
        detail="The task successfully deleted",
    )


@router.patch("/{task_id}", response_model=ResponseCreateNewTask)
async def change_task(
    uow: UOWDep, task_id: uuid.UUID, task: ChangeTaskSchema, account: AccountSchema = Depends(get_current_account)
):
    new_task: TaskSchema = await TaskService().change_task(uow, task, task_id)
    return ResponseDeleteTask(
        status=204,
        error=False,
        payload=new_task,
        detail="The task successfully deleted",
    )
