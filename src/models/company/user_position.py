import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.schemas.company.user_position import UserPositionSchema


class UserPositionModel(BaseModel):
    __tablename__ = "user_position"

    user: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    position: Mapped[int] = mapped_column(
        ForeignKey("position.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
    user_relationship: Mapped["UserModel"] = relationship("UserModel", back_populates="positions")
    position_relationship: Mapped["PositionModel"] = relationship("PositionModel", back_populates="users")

    def to_pydantic_schema(self) -> UserPositionSchema:
        return UserPositionSchema(
            user=self.user,
            position=self.position,
        )