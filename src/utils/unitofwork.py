from abc import ABC, abstractmethod

from src.database.db import async_session_maker
from src.repositories.account import AccountRepository
from src.repositories.company import CompanyRepository
from src.repositories.invite import InviteRepository
from src.repositories.position import PositionRepository
from src.repositories.struct_adm import StructAdmRepository
from src.repositories.struct_adm_position import StructAdmPositionRepository
from src.repositories.task import TaskRepository
from src.repositories.task_user import TaskUserRepository
from src.repositories.user import UserRepository
from src.repositories.members import MembersRepository
from src.repositories.user_position import UserPositionRepository


class IUnitOfWork(ABC):
    user: UserRepository
    account: AccountRepository
    invite: InviteRepository
    company: CompanyRepository
    members: MembersRepository
    task: TaskRepository
    position: PositionRepository
    struct_adm: StructAdmRepository
    user_position: UserPositionRepository
    struct_adm_position: StructAdmPositionRepository
    task_user: TaskUserRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    """The class responsible for the atomicity of transactions"""

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user = UserRepository(self.session)
        self.account = AccountRepository(self.session)
        self.invite = InviteRepository(self.session)
        self.company = CompanyRepository(self.session)
        self.members = MembersRepository(self.session)
        self.task = TaskRepository(self.session)
        self.position = PositionRepository(self.session)
        self.struct_adm = StructAdmRepository(self.session)
        self.user_position = UserPositionRepository(self.session)
        self.struct_adm_position = StructAdmPositionRepository(self.session)
        self.task_user = TaskUserRepository(self.session)

    async def __aexit__(self, exc_type, *args):
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
