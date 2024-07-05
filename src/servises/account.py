import uuid
from fastapi import HTTPException, status

from src.models.company import CompanyModel
from src.models.user import InviteModel, AccountModel, UserModel
from src.schemas.company import CreateCompanySchema
from src.schemas.user import SingUpCompleteSchema, CreateUserSchema, CreateUserSchemaAndEmailAndId
from src.tasks.tasks import send_invite_code_to_email
from pydantic import EmailStr
from src.utils.generator_invite_codes import generator_invite_codes
from src.schemas.user.account import AccountSchema
from src.utils.jwt_utils import hash_password
from src.utils.unitofwork import IUnitOfWork


class AccountService:
    async def checking_account_and_send_invitation(self, uow: IUnitOfWork, email: EmailStr) -> InviteModel:
        async with uow:
            code = generator_invite_codes()
            invite_exist: bool = await uow.account.checking_account_existence(email)
            if not invite_exist:
                invite: InviteModel = await uow.invite.add_one_and_get_obj(email=email, code=code)
                send_invite_code_to_email.delay(email, code)
                return invite
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email already exists")

    async def checking_account(self, uow: IUnitOfWork, email: EmailStr):
        async with uow:
            result = await uow.account.checking_account_existence(email)
            return result

    async def create_company(self, uow: IUnitOfWork, data: SingUpCompleteSchema) -> uuid:
        async with uow:
            company: CompanyModel = await uow.company.add_one_and_get_obj(name=data.company_name)

            user_id = await uow.user.add_one_and_get_id(first_name=data["first_name"], last_name=data["last_name"])
            await uow.members.add_one(user=user_id, company=company.id, admin=True)
            account = await uow.account.add_one_and_get_obj(
                email=data["account"], user_id=user_id, password=hash_password(data["password"])
            )
            return CreateCompanySchema(
                company_id=company.id,
                company_name=company.name,
                admin=user_id,
                email=account.email,
            )

    async def get_one_account(self, uow: IUnitOfWork, account_id: str) -> AccountSchema | list:
        async with uow:
            result = await uow.account.get_one(account_id)
            return result

    async def get_company_id(self, uow: IUnitOfWork, account: AccountSchema) -> uuid.UUID:
        async with uow:
            company_id: uuid.UUID = await uow.account.get_company_id_from_account(account.id)
            return company_id

    async def change_email(
            self,
            uow: IUnitOfWork,
            account_id: uuid.UUID,
            email: EmailStr,
    ):
        data = {"email": email}
        async with uow:
            await uow.account.update_one_by_id(account_id, data)

    async def change_ditail(
            self,
            uow: IUnitOfWork,
            account: AccountSchema,
            new_data: CreateUserSchema,
    ) -> CreateUserSchemaAndEmailAndId:
        async with uow:
            # account.user_id - user_id
            # account.email - email
            account: AccountModel | None = await uow.account.get_by_query_one_or_none(id=account.id)
            if not account:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authorization")
            user: UserModel | None = await uow.user.update_one_by_id(account.user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
            user: UserModel | None = await uow.user.update_one_by_id(
                user.id,
                {
                    "first_name": new_data.first_name,
                    "last_name": new_data.last_name,
                    "middle_name": new_data.middle_name,
                },
            )
            if not user:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CreateUserSchemaAndEmailAndId(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                middle_name=user.middle_name,
                email=account.email,
            )

    async def add_user_password(
            self,
            uow: IUnitOfWork,
            user_id: uuid.UUID,
            email: EmailStr,
            password: str
    ) -> CreateUserSchemaAndEmailAndId:
        async with uow:
            check_account: bool = await uow.account.checking_account_existence(email)
            if check_account:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This user already exist")
            await uow.account.add_one(
                email=email,
                user_id=user_id,
                password=hash_password(password)
            )
            user: UserModel | None = await uow.user.get_by_query_one_or_none(user_id=user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user doesnt exist")
            return CreateUserSchemaAndEmailAndId(
                first_name=user.first_name,
                last_name=user.last_name,
                middle_name=user.middle_name,
                id=user_id,
                email=email,
            )
