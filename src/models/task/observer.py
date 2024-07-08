import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel


class ObserverModel(BaseModel):
    __tablename__ = "observer"

    user: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    task: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
