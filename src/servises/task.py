import uuid
from fastapi import HTTPException, status
from src.models import TaskModel
from src.schemas.task import CreateTaskSchema, TaskSchema
from src.schemas.task.task import DeleteTaskSchema, ChangeTaskSchema
from src.schemas.user import AccountSchema
from src.utils.unitofwork import IUnitOfWork


class TaskService:
    async def create_task(
        self,
        uow: IUnitOfWork,
        task: CreateTaskSchema,
        account: AccountSchema,
    ) -> TaskSchema:
        async with uow:
            new_task: TaskModel = await uow.task.add_one_and_get_obj(
                title=task.title,
                description=task.description,
                responsible=task.responsible,
                observers=task.observers,
                performers=task.performers,
                deadline=task.deadline,
                status=task.status,
                execution_time=task.execution_time,
            )
            return new_task.to_pydantic_schema()

    async def delete_task(
        self,
        uow: IUnitOfWork,
        task_id: uuid.UUID,
    ) -> DeleteTaskSchema:
        async with uow:
            task: TaskModel | None = await uow.task.get_by_query_one_or_none(
                id=task_id,
            )
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This task doesn't exist")
            task_name = task.title
            await uow.task.delete_by_query(id=task_id)
            return DeleteTaskSchema(title=task_name)

    async def change_task(self, uow: IUnitOfWork, new_task: ChangeTaskSchema, task_id: uuid.UUID) -> TaskSchema:
        async with uow:
            task_dict = {}
            for field, value in new_task.model_dump().items():
                if value:
                    task_dict[field] = value
            task: TaskModel | None = await uow.task.update_one_by_id(
                task_id,
                task_dict,
            )
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This task doesn't exist")
            return task.to_pydantic_schema()
