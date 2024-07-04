from src.models.user import InviteModel
from src.utils.repository import SqlAlchemyRepository


class InviteRepository(SqlAlchemyRepository):
    model = InviteModel
