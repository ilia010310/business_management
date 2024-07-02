import uuid

from pydantic import EmailStr

from src.utils.unitofwork import IUnitOfWork


class AccountService:
    async def checking_account_and_send_invitation(self, uow: IUnitOfWork, email: EmailStr, code: int):
        async with uow:
            result = await uow.account.checking_account_existence(email)
            if not result:
                await uow.invite.add_one(email=email, code=code)
            return result

    async def create_company(self, uow: IUnitOfWork, data: dict) -> uuid:
        async with uow:
            company_id = await uow.company.add_one_and_get_obj(name=data["company_name"])

            user_id = await uow.user.add_one_and_get_obj(
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
            await uow.members.add_one(
                user=user_id,
                company=company_id,
                admin=True
            )
            account = await uow.account.add_one_and_get_obj(email=data['account'], user_id=user_id)
            return account

