from pydantic import EmailStr

from src.schemas.sing_up import SingUpSchema
from src.utils.unitofwork import IUnitOfWork


class InviteService:
    async def checking_invitation(
        self,
        uow: IUnitOfWork,
        data: SingUpSchema,
    ) -> list:
        async with uow:
            result: list = await uow.invite.checking_invitation(dict(data))
            return result
