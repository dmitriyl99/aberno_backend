"""Add is active for users

Revision ID: 015734dc9af3
Revises: 6ed544830b63
Create Date: 2024-05-02 15:35:16.849465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '015734dc9af3'
down_revision: Union[str, None] = '6ed544830b63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_active', sa.Boolean, default=True))


def downgrade() -> None:
    op.drop_column('users', 'is_active')
