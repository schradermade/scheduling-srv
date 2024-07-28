"""Create phone number for user column2

Revision ID: 6ce00f5d1b3d
Revises: 82a14df63dbf
Create Date: 2024-07-27 15:11:55.941809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ce00f5d1b3d'
down_revision: Union[str, None] = '82a14df63dbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
