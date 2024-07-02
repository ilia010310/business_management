import uuid
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.models import BaseModel, members
from src.models.company import CompanyModel
from src.models.mixins.custom_types import (
    uuid_pk_T,
    created_at_T,
    updated_at_T,
    str_50_T,
    str_50_or_none_T,
)
from src.schemas.user import UserSchema


class SecretsModel(BaseModel):
    __tablename__ = "secrets"

    id: Mapped[uuid_pk_T]
    password = Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("UserModel", back_populates="secrets")
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False)
    account = relationship("AccountModel", back_populates="secrets")
