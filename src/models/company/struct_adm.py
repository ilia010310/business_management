from typing import Any

from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database.db import async_engine
from src.models.base import BaseModel
from src.models.mixins.custom_types import (
    str_50_T,
)
from sqlalchemy import Sequence, Index, Column, Integer, String
from sqlalchemy import func
from sqlalchemy.orm import relationship, remote, foreign
from sqlalchemy_utils import LtreeType, Ltree

# class StructAdmModel(BaseModel):
#     __tablename__ = "struct_adm"
#
#     name: Mapped[str_50_T] = mapped_column(nullable=False, primary_key=True)
#     path: LtreeType = mapped_column(nullable=False)


id_seq = Sequence('nodes_id_seq')


class StructAdmModel(BaseModel):
    __tablename__ = 'struct_adm'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    path = Column(LtreeType, nullable=False)

    positions: Mapped[list["StructAdmPositionModel"]] = relationship("StructAdmPositionModel",
                                                                     back_populates="struct_adm")

    parent = relationship(
        'StructAdmModel',
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref='children',
        viewonly=True
    )

    def __init__(self, name, parent=None, **kw: Any):
        super().__init__(**kw)
        _id = async_engine.execute(id_seq)
        self.id = _id
        self.name = name
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id

    __table_args__ = (
        Index('ix_nodes_path', path, postgresql_using='gist'),
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Node({})'.format(self.name)
