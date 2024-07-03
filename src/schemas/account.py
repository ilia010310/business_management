import uuid

from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: uuid.UUID
    email: str

