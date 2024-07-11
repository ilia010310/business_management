

from src.models import StructAdmPositionModel
from src.utils.repository import SqlAlchemyRepository


class StructAdmPositionRepository(SqlAlchemyRepository):
    model = StructAdmPositionModel
