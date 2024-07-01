from src.schemas.user import CreateUserSchema
from src.utils.unitofwork import IUnitOfWork


class UserService:
    async def add_one(self, uow: IUnitOfWork, employee: CreateUserSchema):
        async with uow:
            result = await uow.user.add_one(dict(employee))
