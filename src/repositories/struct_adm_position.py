

from src.models import StructAdmPositionModel
from src.utils.repository import SqlAlchemyRepository


class StructAdmPosition(SqlAlchemyRepository):
    model = StructAdmPositionModel
