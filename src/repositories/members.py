from sqlalchemy import select, Result
import uuid

from src.models import MembersModel
from src.utils.repository import SqlAlchemyRepository


class MembersRepository(SqlAlchemyRepository):
    model = MembersModel

    async def get_company_id_from_members(self, user_id: uuid.UUID) -> uuid.UUID:
        query = select(self.model.company).where(self.model.user == user_id)
        result: Result = await self.session.execute(query)
        company_id: uuid.UUID = result.scalars().all()[0]
        return company_id
