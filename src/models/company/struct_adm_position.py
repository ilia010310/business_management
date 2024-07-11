import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.schemas.company.struct_adm_position import StructAdmPositionSchema


class StructAdmPositionModel(BaseModel):
    __tablename__ = "struct_adm_position"

    struct_adm_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("struct_adm.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
    position_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("position.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
    struct_adm: Mapped["StructAdmModel"] = relationship("StructAdmModel", back_populates="positions")
    position: Mapped["PositionModel"] = relationship("PositionModel", back_populates="struct_adm_positions")

    def to_pydantic_schema(self) -> StructAdmPositionSchema:
        return StructAdmPositionSchema(
            struct_adm_id=self.struct_adm_id,
            position_id=self.position_id
        )

