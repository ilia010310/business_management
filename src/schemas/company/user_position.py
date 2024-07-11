import uuid

from pydantic import BaseModel


class UserPositionSchema(BaseModel):
    user: uuid.UUID
    position: int
