from sqlalchemy.orm import Mapped, relationship

from src.models.base import BaseModel
from src.models.mixins.custom_types import (
    uuid_pk_T,
    created_at_T,
    updated_at_T,
    str_50_T,
    int_or_none,
)
from src.schemas.company.company import CompanySchema


class CompanyModel(BaseModel):
    __tablename__ = "company"

    id: Mapped[uuid_pk_T]
    name: Mapped[str_50_T]
    inn: Mapped[int_or_none]
    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]
    users: Mapped[list["UserModel"]] = relationship("UserModel", back_populates="companies", secondary="members")

    def to_pydantic_schema(self) -> CompanySchema:
        return CompanySchema(
            id=self.id,
            name=self.name,
        )
