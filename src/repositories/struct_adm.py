from typing import Sequence, Any

from sqlalchemy import text, Row, Result, select

from src.models import StructAdmModel
from src.utils.repository import SqlAlchemyRepository


class StructAdmRepository(SqlAlchemyRepository):
    model = StructAdmModel

    async def get_children_paths(self, struct_adm_id: int) -> Sequence[Row[tuple[Any, ...] | Any]]:
        query = text(
            "SELECT id, name, path FROM struct_adm WHERE path <@ (SELECT path FROM struct_adm WHERE id = :node_id)"
        ).params(node_id=struct_adm_id)
        result: Result = await self.session.execute(query)
        child_nodes = result.fetchall()
        return child_nodes

    async def change_children_paths(self, child_nodes: Sequence[Row[tuple[Any, ...] | Any]]) -> None:
        node_name = child_nodes[0][1]
        for child in child_nodes[1:]:
            child_id, child_name, child_path = child
            new_path = child_path.replace(f"{node_name}.", "")
            stmt = text(
                "UPDATE struct_adm SET path = :new_path WHERE id = :child_id",
            ).params({"new_path": new_path, "child_id": child_id})
            await self.session.execute(stmt)

    async def get_all_path_of_parent(self, parent: str) -> type(model) | None:
        query = select(self.model.path).where(self.model.name == parent)
        path: Result | None = await self.session.execute(query)
        return path.scalar_one_or_none()
