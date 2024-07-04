import uuid

from src.schemas.user import CreateUserSchema
from src.utils.unitofwork import IUnitOfWork


class UserService:
    async def add_one(self, uow: IUnitOfWork, employee: CreateUserSchema):
        async with uow:
            result = await uow.user.add_one_and_get_obj(**dict(employee))
            return result

    async def change_names(
            self,
            uow: IUnitOfWork,
            user_id: uuid.UUID,
            data: CreateUserSchema
    ) -> None:
        async with uow:
            await uow.user.update_one_by_id(user_id, dict(data))
