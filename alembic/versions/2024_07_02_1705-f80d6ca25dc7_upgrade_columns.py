"""Upgrade columns

Revision ID: f80d6ca25dc7
Revises: 5e3cf23093c2
Create Date: 2024-07-02 17:05:30.112631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f80d6ca25dc7'
down_revision: Union[str, None] = '5e3cf23093c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###