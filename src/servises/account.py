import uuid

from pydantic import EmailStr

from src.schemas.account import AccountSchema
from src.utils.jwt_utils import hash_password
from src.utils.unitofwork import IUnitOfWork


class AccountService:
    async def checking_account_and_send_invitation(self, uow: IUnitOfWork, email: EmailStr, code: int):
        async with uow:
            result = await uow.account.checking_account_existence(email)
            if not result:
                await uow.invite.add_one(email=email, code=code)
            return result

    async def checking_account(self, uow: IUnitOfWork, email: EmailStr):
        async with uow:
            result = await uow.account.checking_account_existence(email)
            return result

    async def create_company(self, uow: IUnitOfWork, data: dict) -> uuid:
        async with uow:
            company_id: uuid.UUID = await uow.company.add_one_and_get_id(name=data["company_name"])

            user_id = await uow.user.add_one_and_get_obj(
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
            await uow.members.add_one(
                user=user_id,
                company=company_id,
                admin=True
            )
            account = await uow.account.add_one_and_get_obj(
                email=data['account'],
                user_id=user_id,
                password=hash_password(data['password'])
            )
            return account

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
