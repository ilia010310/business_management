import uuid

from fastapi import HTTPException, status
from pydantic import EmailStr

from src.config import settings
from src.schemas.user.user import CreateUserSchemaAndEmail
from src.tasks.tasks import send_invite_code_to_email, send_invite_link_to_email

from src.models.user import UserModel, InviteModel
from src.schemas.user import CreateUserSchema, CreateUserSchemaAndEmailAndId, AccountSchema, RequestChangeEmailSchema
from src.utils.generator_invite_codes import generator_invite_codes
from src.utils.unitofwork import IUnitOfWork


class UserService:
    async def add_one_user_for_company(
            self, uow: IUnitOfWork, employee: CreateUserSchemaAndEmail, account: AccountSchema
    ) -> CreateUserSchemaAndEmailAndId:
        async with uow:
            invite_exist: bool = await uow.account.checking_account_existence(employee.email)
            if invite_exist:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email already exists")
            user: UserModel = await uow.user.add_one_and_get_obj(
                first_name=employee.first_name, last_name=employee.last_name, middle_name=employee.middle_name
            )
            link = f"{settings.BASE_URL}/api/auth/v1/complete_sing_up/{user.id}/{employee.email}"
            send_invite_link_to_email.delay(employee.email, link)
            admin_user_id: uuid.UUID = await uow.account.get_user_id_from_account(account.id)
            company_id: uuid.UUID = await uow.members.get_company_id_from_members(admin_user_id)

            await uow.members.add_one(user=user.id, company=company_id)
            return CreateUserSchemaAndEmailAndId(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                middle_name=user.middle_name,
                email=employee.email,
            )

    async def change_names(self, uow: IUnitOfWork, user_id: uuid.UUID, data: CreateUserSchema) -> None:
        async with uow:
            await uow.user.update_one_by_id(user_id, dict(data))

    async def request_for_change_email(
            self,
            uow: IUnitOfWork,
            new_email: EmailStr,
            account: AccountSchema,
    ) -> RequestChangeEmailSchema:
        async with uow:
            code = generator_invite_codes()
            invite_exist: bool = await uow.account.checking_account_existence(new_email)
            if not invite_exist:
                invite: InviteModel = await uow.invite.add_one_and_get_obj(email=new_email, code=code)
                send_invite_code_to_email.delay(new_email, code)
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email already exists")
            user_id = await uow.user.get_user_id_from_account(account.id)
            if not user_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User in not found")
            return RequestChangeEmailSchema(
                old_email=account.email,
                new_email=new_email,
                user_id=user_id,
            )
