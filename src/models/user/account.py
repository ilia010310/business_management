import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.models import BaseModel

from src.models.mixins.custom_types import uuid_pk_T, str_50_T
from src.schemas.user import AccountSchema


class AccountModel(BaseModel):
    __tablename__ = "account"

    id: Mapped[uuid_pk_T]
    email: Mapped[str_50_T] = mapped_column(unique=True, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), unique=True)
    password: Mapped[bytes]
    active: Mapped[bool] = mapped_column(default=True)

    def to_pydantic_schema(self) -> AccountSchema:
        return AccountSchema(
            id=self.id,
            username=self.email,
            password=self.password,
            active=self.active,
        )
