from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep
from src.api.user.v1.dependencies.jwt_dependencies import get_current_account
from src.schemas.response import ResponseCreateNewTask
from src.schemas.task import CreateTaskSchema, TaskSchema
from src.schemas.user import AccountSchema
from src.servises.task import TaskService

router = APIRouter(prefix="/task/v1", tags=["Tasks operations"])


@router.post("/create", response_model=ResponseCreateNewTask)
async def create_task(uow: UOWDep, task: CreateTaskSchema, account: AccountSchema = Depends(get_current_account)):
    task: TaskSchema = await TaskService().create_task(uow, task, account)
    return ResponseCreateNewTask(
        status=201,
        error=False,
        payload=task,
        detail="The task successfully created",
    )

