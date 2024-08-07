
from sqlalchemy.orm import Mapped, relationship
from src.models import BaseModel
from src.models.mixins.custom_types import (
    uuid_pk_T,
    created_at_T,
    updated_at_T,
    str_50_T,
    str_50_or_none_T,
)
from src.schemas.user import UserSchema


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[uuid_pk_T]
    first_name: Mapped[str_50_T]
    last_name: Mapped[str_50_T]
    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]
    middle_name: Mapped[str_50_or_none_T]
    companies: Mapped[list["CompanyModel"]] = relationship("CompanyModel", back_populates="users", secondary="members")

    def to_pydantic_schema(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
        )
