from sqlalchemy.orm import Mapped

from src.models import BaseModel
from src.models.mixins.custom_types import (
    uuid_pk_T,
    created_at_T,
    updated_at_T,
    str_50_T,
)
from src.schemas.company import CompanySchema


class UserModel(BaseModel):
    __tablename__ = 'company'

    id: Mapped[uuid_pk_T]
    name: Mapped[str_50_T]
    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    def to_pydantic_schema(self) -> CompanySchema:
        return CompanySchema(
            id=self.id,
            first_name=self.name,
        )
