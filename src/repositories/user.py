import uuid

from sqlalchemy import delete, select, Result

from src.models.user import UserModel
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = UserModel

    async def delete_users(self, users_id: list[uuid.UUID]) -> None:
        stmt = delete(self.model).where(self.model.id.in_(users_id))
        await self.session.execute(stmt)


