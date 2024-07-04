from sqlalchemy.orm import Mapped
from src.models import BaseModel
from src.models.mixins.custom_types import (
    uuid_pk_T,
    created_at_T,
    updated_at_T,
    str_50_T,
)


class InviteModel(BaseModel):
    __tablename__ = "invite"

    id: Mapped[uuid_pk_T]
    email: Mapped[str_50_T]
    code: Mapped[int]
    created_at: Mapped[created_at_T]

