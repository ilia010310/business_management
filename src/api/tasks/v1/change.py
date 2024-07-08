import uuid

from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep
from src.api.user.v1.dependencies.jwt_dependencies import get_current_account
from src.schemas.response import ResponseCreateNewTask

from src.schemas.response.task.delete import ResponseDeleteTask

from src.schemas.task.task import DeleteTaskSchema, ChangeTaskSchema, TaskSchema
from src.schemas.user import AccountSchema
from src.servises.task import TaskService

router = APIRouter(prefix="/task/v1", tags=["Tasks operations"])


@router.patch("/change/{task_id}", response_model=ResponseCreateNewTask)
async def change_task(uow: UOWDep, task_id: uuid.UUID, task: ChangeTaskSchema,
                      account: AccountSchema = Depends(get_current_account)):
    new_task: TaskSchema = await TaskService().change_task(uow, task, task_id)
    return ResponseDeleteTask(
        status=204,
        error=False,
        payload=task,
        detail="The task successfully deleted",
    )
