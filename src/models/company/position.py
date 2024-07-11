import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import BaseModel
from src.models.mixins.custom_types import (
    str_50_T,
)
from src.schemas.company.position import PositionSchema


class PositionModel(BaseModel):
    __tablename__ = "position"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_50_T] = mapped_column(unique=True, nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    company = relationship("CompanyModel", back_populates="positions")
    struct_adm_positions: Mapped[list["StructAdmPositionModel"]] = relationship(
        "StructAdmPositionModel", back_populates="position"
    )

    def to_pydantic_schema(self) -> PositionSchema:
        return PositionSchema(
            id=self.id,
            name=self.name,
            company_id=self.company_id,
        )
