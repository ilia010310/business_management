import uuid

from pydantic import BaseModel


class CreateMembersSchema(BaseModel):
    user: uuid.UUID
    company: uuid.UUID
