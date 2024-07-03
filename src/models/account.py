import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.models import BaseModel

from src.models.mixins.custom_types import uuid_pk_T, str_50_T


class AccountModel(BaseModel):
    __tablename__ = "account"

    id: Mapped[uuid_pk_T]
    email: Mapped[str_50_T]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), unique=True)
    password: Mapped[bytes]
