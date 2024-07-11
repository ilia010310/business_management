import uuid

from pydantic import BaseModel


class TaskUsersSchema(BaseModel):
    user: uuid.UUID
    task: uuid.UUID
    role: str
