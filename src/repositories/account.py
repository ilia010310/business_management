import uuid

from pydantic import EmailStr
from sqlalchemy import delete, select, Result

from src.models.user import AccountModel
from src.utils.repository import SqlAlchemyRepository


class AccountRepository(SqlAlchemyRepository):
    model = AccountModel

    async def delete_accounts(self, users_id: list[uuid.UUID]) -> None:
        stmt = delete(self.model).where(self.model.user_id.in_(users_id))
        await self.session.execute(stmt)

    async def get_user_id_from_account(self, account_id: uuid.UUID) -> uuid.UUID:
        query = select(self.model.user_id).where(self.model.id == account_id)
        user_id: Result | None = await self.session.execute(query)
        return user_id.scalar_one_or_none()

    async def checking_account_existence(self, email: EmailStr) -> bool:
        query = select(self.model).where(self.model.email == email)
        res: Result = await self.session.execute(query)
        account = list(res.scalars().all())
        if account:
            return True
        return False
