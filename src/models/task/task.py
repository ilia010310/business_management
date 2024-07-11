import uuid
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.models import BaseModel
from src.models.mixins.custom_types import (
    uuid_pk_T,
    str_50_T,
)
from src.schemas.task import TaskSchema


class TaskModel(BaseModel):
    __tablename__ = "task"

    id: Mapped[uuid_pk_T]
    title: Mapped[str_50_T]
    description: Mapped[str]
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    responsible_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    author: Mapped["UserModel"] = relationship("UserModel", foreign_keys=[author_id])
    responsible: Mapped["UserModel"] = relationship("UserModel", foreign_keys=[responsible_id])
    deadline: Mapped[datetime]
    status: Mapped[str]
    execution_time: Mapped[timedelta]
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    company = relationship("CompanyModel", back_populates="tasks")

    def to_pydantic_schema(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            author=self.author_id,
            responsible=self.responsible_id,
            observers=self.observers,
            performers=self.performers,
            deadline=self.deadline,
            status=self.status,
            execution_time=self.execution_time,
        )
