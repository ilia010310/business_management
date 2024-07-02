from src.models import CompanyModel
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = CompanyModel
