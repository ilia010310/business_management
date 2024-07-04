import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from src.models.mixins.custom_types import created_at_T


class InviteSchema(BaseModel):

    id: uuid.UUID
    email: EmailStr
    code: int
    created_at: datetime
