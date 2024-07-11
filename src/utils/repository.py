import uuid
from abc import ABC, abstractmethod
from typing import Sequence, Union, Tuple, Any
from uuid import uuid4

from pydantic import EmailStr
from sqlalchemy import insert, select, update, delete, and_, text, Row
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_id(self, *args, **kwargs):
        raise NotImplementedError

    async def add_one_and_get_obj(self, *args, **kwargs):
        raise NotImplementedError

    async def get_by_query_one_or_none(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_by_query_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_id(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_query(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    """
    A basic repository that implements basic CRUD
    functions with a base table using the SqlAlchemy library

    params:
        - model: SQLAlchemy DeclarativeBase child class
    """

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, **kwargs) -> None:
        query = insert(self.model).values(**kwargs)
        await self.session.execute(query)

    async def add_one_and_get_id(self, **kwargs) -> Union[int, str, uuid4]:
        query = insert(self.model).values(**kwargs).returning(self.model.id)
        _id: Result = await self.session.execute(query)
        return _id.scalar_one()

    async def add_one_and_get_obj(self, **kwargs) -> type(model):
        query = insert(self.model).values(**kwargs).returning(self.model)
        _obj: Result = await self.session.execute(query)
        return _obj.scalar_one()

    async def get_by_query_one_or_none(self, **kwargs) -> type(model) | None:
        query = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_by_query_all(self, **kwargs) -> Sequence[type(model)]:
        query = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def update_one_by_id(self, _id: Union[int, str, uuid4], values: dict) -> type(model) | None:
        query = update(self.model).filter(self.model.id == _id).values(**values).returning(self.model)
        _obj: Result | None = await self.session.execute(query)
        return _obj.scalar_one_or_none()

    async def delete_by_query(self, **kwargs) -> None:
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)

    async def delete_all(self) -> None:
        query = delete(self.model)
        await self.session.execute(query)

    async def checking_account_existence(self, email: EmailStr) -> bool:
        query = select(self.model).where(self.model.email == email)
        res: Result = await self.session.execute(query)
        account = list(res.scalars().all())
        if account:
            return True
        return False

    async def checking_invitation(self, data: dict) -> list:
        query = select(self.model).where(
            and_(self.model.email == data["account"], self.model.code == data["invite_token"])
        )
        result: Result = await self.session.execute(query)
        res = list(result.scalars().all())
        return res

    async def get_one(self, id: str):
        query = select(self.model).where(self.model.id == id)
        result: Result = await self.session.execute(query)
        res = result.scalars().all()
        if res:
            return res[0]
        return []

    async def get_user_id_from_account(self, account_id: uuid.UUID) -> uuid.UUID:
        query = select(self.model.user_id).where(self.model.id == account_id)
        user_id: Result | None = await self.session.execute(query)
        return user_id.scalar_one_or_none()

    async def get_company_id_from_members(self, user_id: uuid.UUID) -> uuid.UUID:
        query = select(self.model.company).where(self.model.user == user_id)
        result: Result = await self.session.execute(query)
        company_id: uuid.UUID = result.scalars().all()[0]
        return company_id

    async def get_email_from_code(self, code: int) -> EmailStr:
        query = select(self.model.email).where(self.model.code == code)
        email: Result | None = await self.session.execute(query)
        return email.scalar_one_or_none()

    async def get_all_path_of_parent(self, parent: str) -> type(model) | None:
        query = select(self.model.path).where(self.model.name == parent)
        path: Result | None = await self.session.execute(query)
        return path.scalar_one_or_none()

    async def get_children_paths(self, struct_adm_id: int) -> Sequence[Row[tuple[Any, ...] | Any]]:
        query = text(
            "SELECT id, name, path FROM struct_adm WHERE path <@ (SELECT path FROM struct_adm WHERE id = :node_id)"
        ).params(node_id=struct_adm_id)
        result: Result = await self.session.execute(query)
        child_nodes = result.fetchall()
        return child_nodes

    async def change_children_paths(self, child_nodes: Sequence[Row[tuple[Any, ...] | Any]]) -> None:
        node_path = child_nodes[0][1]
        for child in child_nodes[1:]:
            child_id, child_name, child_path = child
            new_path = child_path.replace(f"{node_path}.", "")
            stmt = text(
                "UPDATE struct_adm SET path = :new_path WHERE id = :child_id",
            ).params({"new_path": new_path, "child_id": child_id})
            await self.session.execute(stmt)

    async def delete_accounts(self, users_id: list[uuid.UUID]) -> None:
        stmt = delete(self.model).where(self.model.user_id.in_(users_id))
        await self.session.execute(stmt)

    async def delete_users(self, users_id: list[uuid.UUID]) -> None:
        stmt = delete(self.model).where(self.model.id.in_(users_id))
        await self.session.execute(stmt)