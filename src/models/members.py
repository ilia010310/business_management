import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel
from src.models.mixins.custom_types import uuid_pk_T


class MembersModel(BaseModel):
    __tablename__ = "members"

    user: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    company: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
    admin: Mapped[bool] = mapped_column(default=False)
