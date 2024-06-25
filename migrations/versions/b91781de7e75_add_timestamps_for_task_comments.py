"""add timestamps for task comments

Revision ID: b91781de7e75
Revises: ccaa75804d27
Create Date: 2024-06-25 17:56:39.953406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b91781de7e75'
down_revision: Union[str, None] = 'ccaa75804d27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('task_comments', sa.Column('created_at', sa.DateTime(), nullable=True),)
    op.add_column('task_comments', sa.Column('updated_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('task_comments', 'created_at')
    op.drop_column('task_comments', 'updated_at')
