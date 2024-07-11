from src.models import StructAdmModel
from src.utils.repository import SqlAlchemyRepository


class StructAdmRepository(SqlAlchemyRepository):
    model = StructAdmModel
