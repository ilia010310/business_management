from pydantic import EmailStr
from fastapi import HTTPException, status
from src.models.user import InviteModel, AccountModel
from src.schemas.user import RequestChangeEmailSchema, AccountSchema
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

    async def check_and_change_email(
        self,
        uow: IUnitOfWork,
        code: int,
        account: AccountSchema,
    ) -> RequestChangeEmailSchema:
        async with uow:
            email: EmailStr = await uow.invite.get_email_from_code(code)
            if not email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code is invalid")
            new_account: AccountModel = await uow.account.update_one_by_id(account.id, {"email": email})
            return RequestChangeEmailSchema(
                old_email=account.username,
                new_email=new_account.email,
                user_id=new_account.user_id,
            )
