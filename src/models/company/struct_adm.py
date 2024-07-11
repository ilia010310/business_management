import uuid

from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import BaseModel

from sqlalchemy import Sequence, Column, Integer, String, ForeignKey
from sqlalchemy_utils import LtreeType

from src.schemas.company.struct_adm import StructAdmSchema


id_seq = Sequence("nodes_id_seq")


class StructAdmModel(BaseModel):
    __tablename__ = "struct_adm"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False, unique=True)
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), nullable=False)

    path = Column(LtreeType, nullable=False, unique=True)

    positions: Mapped[list["StructAdmPositionModel"]] = relationship(
        "StructAdmPositionModel", back_populates="struct_adm"
    )

    def to_pydantic_schema(self) -> StructAdmSchema:
        return StructAdmSchema(
            id=self.id,
            name=self.name,
            company_id=self.company_id,
            path=str(self.path),
        )
