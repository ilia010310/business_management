import uuid

from pydantic import BaseModel


class CreateNewStructAdmSchema(BaseModel):
    name: str
    parent: str


class StructAdmSchema(BaseModel):
    id: int
    name: str
    company_id: uuid.UUID
    path: str
