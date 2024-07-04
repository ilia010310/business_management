import uuid

from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: uuid.UUID
    username: str
    password: bytes
    active: bool


class CreateAccountSchema(BaseModel):
    id: uuid.UUID
    email: str
