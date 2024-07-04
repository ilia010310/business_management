from pydantic import EmailStr
from fastapi import HTTPException, status
from src.models.user import InviteModel
from src.schemas.user.sing_up import SingUpSchema
from src.utils.unitofwork import IUnitOfWork


class InviteService:
    async def checking_invitation(
            self,
            uow: IUnitOfWork,
            data: SingUpSchema,
    ) -> InviteModel | None:
        async with uow:
            invite: InviteModel | None = await uow.invite.get_by_query_one_or_none(
                account=data.account,
                invite_token=data.invite_token,
            )
            if not invite:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email or code is not valid")
            return invite

    async def get_email(
            self,
            uow: IUnitOfWork,
            code: int,
    ) -> EmailStr:
        async with uow:
            email: EmailStr = await uow.invite.get_email_from_code(code)
            return email
