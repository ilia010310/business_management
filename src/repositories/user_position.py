from src.models import UserPositionModel
from src.utils.repository import SqlAlchemyRepository


class UserPositionRepository(SqlAlchemyRepository):
    model = UserPositionModel
