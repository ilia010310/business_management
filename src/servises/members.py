import uuid

from src.schemas.members import CreateMembersSchema
from src.utils.unitofwork import IUnitOfWork


class MembersService:

    async def get_company_id_from_members(self, uow: IUnitOfWork, user_id) -> uuid.UUID:
        async with uow:
            company_id: uuid.UUID = await uow.members.get_company_id_from_members(user_id)
            return company_id

    async def add_one(self, uow: IUnitOfWork, data: CreateMembersSchema) -> None:
        async with uow:
            await uow.members.add_one(**dict(data))

