from src.models import MembersModel
from src.utils.repository import SqlAlchemyRepository


class MembersRepository(SqlAlchemyRepository):
    model = MembersModel