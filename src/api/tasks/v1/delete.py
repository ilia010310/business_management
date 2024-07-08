import uuid

from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep
from src.api.user.v1.dependencies.jwt_dependencies import get_current_account

from src.schemas.response.task.delete import ResponseDeleteTask

from src.schemas.task.task import DeleteTaskSchema
from src.schemas.user import AccountSchema
from src.servises.task import TaskService

router = APIRouter(prefix="/task/v1", tags=["Tasks operations"])


@router.get("/delete/{task_id}", response_model=ResponseDeleteTask)
async def delete_task(uow: UOWDep, task_id: uuid.UUID, account: AccountSchema = Depends(get_current_account)):
    task: DeleteTaskSchema = await TaskService().delete_task(uow, task_id)
    return ResponseDeleteTask(
        status=204,
        error=False,
        payload=task,
        detail="The task successfully deleted",
    )

