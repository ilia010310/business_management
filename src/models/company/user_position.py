import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel


class UserPositionModel(BaseModel):
    __tablename__ = "user_position"

    user: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    position: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("position.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
