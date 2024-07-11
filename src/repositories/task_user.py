from sqlalchemy import text

from src.models import TaskUsersModel

from src.utils.repository import SqlAlchemyRepository


class TaskUserRepository(SqlAlchemyRepository):
    model = TaskUsersModel

    async def add_users_to_task_users(
            self,
            roles_list: list[dict]
    ) -> None:
        values_str = ', '.join([f"('{data['user']}', {data['task']}, {data['role']})" for data in roles_list])
        stmt = text(f"""
               INSERT INTO tasks_users (user, task, role)
               VALUES {values_str}
           """)
        await self.session.execute(stmt)
