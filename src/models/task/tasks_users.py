import uuid
from sqlalchemy import Enum, PrimaryKeyConstraint
from enum import Enum as PyEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel


class Role(PyEnum):
    OBSERVER = "observer"
    PERFORMER = "performer"


class TasksUsersModel(BaseModel):
    __tablename__ = "tasks_users"

    user: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    task: Mapped[uuid.UUID] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("user", "task", "role"),)
