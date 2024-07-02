from src.models import AccountModel
from src.utils.repository import SqlAlchemyRepository


class AccountRepository(SqlAlchemyRepository):
    model = AccountModel
