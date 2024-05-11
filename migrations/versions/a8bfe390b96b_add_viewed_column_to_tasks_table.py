"""Add viewed column to tasks table

Revision ID: a8bfe390b96b
Revises: f9f39e35dea8
Create Date: 2024-05-11 14:39:52.783726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8bfe390b96b'
down_revision: Union[str, None] = 'f9f39e35dea8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'tasks',
        sa.Column('viewed', sa.Boolean, default=False)
    )
    op.alter_column('tasks', 'deadline', type_=sa.DateTime())


def downgrade() -> None:
    op.drop_column(
        'tasks', 'viewed'
    )
    op.alter_column('tasks', 'deadline', type_=sa.Date())
