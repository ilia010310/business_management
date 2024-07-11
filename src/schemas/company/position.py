import uuid

from pydantic import BaseModel


class CreatePositionSchema(BaseModel):
    name: str


class PositionSchema(CreatePositionSchema):
    id: int
    company_id: uuid.UUID
