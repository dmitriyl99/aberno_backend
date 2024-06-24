"""make deadline in task as period

Revision ID: ccaa75804d27
Revises: 360269b3203e
Create Date: 2024-06-24 16:47:14.213418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccaa75804d27'
down_revision: Union[str, None] = '360269b3203e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('deadline_end', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('tasks', 'deadline_end')
