"""add viewed_at column to tasks table

Revision ID: 466782bf0aa3
Revises: 2e10b435dd57
Create Date: 2024-05-21 19:29:58.677709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '466782bf0aa3'
down_revision: Union[str, None] = '2e10b435dd57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('viewed_at', sa.DateTime, nullable=True, default=None))


def downgrade() -> None:
    op.drop_column('tasks', 'viewed_at')
