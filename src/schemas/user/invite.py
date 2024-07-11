import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr



class InviteSchema(BaseModel):
    id: uuid.UUID
    email: EmailStr
    code: int
    created_at: datetime
