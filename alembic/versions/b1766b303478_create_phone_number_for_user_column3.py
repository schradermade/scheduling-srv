"""Create phone number for user column3

Revision ID: b1766b303478
Revises: 6ce00f5d1b3d
Create Date: 2024-07-27 15:12:54.352806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1766b303478'
down_revision: Union[str, None] = '6ce00f5d1b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(length=15), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
