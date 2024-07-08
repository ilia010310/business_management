import uuid
from datetime import datetime, timedelta
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from src.models import UserModel


class TaskSchema(BaseModel):
    id: uuid.UUID
    title: str = Field(max_length=50)
    description: str
    author: uuid.UUID
    responsible: uuid.UUID
    observers: list[uuid.UUID]
    performers: list[uuid.UUID]
    deadline: datetime
    status: str
    execution_time: timedelta


class CreateTaskSchema(BaseModel):
    title: str = Field(max_length=50)
    description: str
    responsible: uuid.UUID
    observers: list[uuid.UUID]
    performers: list[uuid.UUID]
    deadline: datetime
    status: str
    execution_time: timedelta


class DeleteTaskSchema(BaseModel):
    title: str


class ChangeTaskSchema(BaseModel):
    title: Annotated[Optional[str], Field(default=None)]
    description: Annotated[Optional[str], Field(default=None)]
    responsible: Annotated[Optional[uuid.UUID], Field(default=None)]
    observers: Annotated[Optional[list[uuid.UUID]], Field(default=None)]
    performers: Annotated[Optional[list[uuid.UUID]], Field(default=None)]
    deadline: Annotated[Optional[datetime], Field(default=None)]
    status: Annotated[Optional[str], Field(default=None)]
    execution_time: Annotated[Optional[timedelta], Field(default=None)]
