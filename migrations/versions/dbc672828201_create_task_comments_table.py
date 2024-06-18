"""Create task_comments table

Revision ID: dbc672828201
Revises: fb416f7b214e
Create Date: 2024-06-18 23:01:15.661931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbc672828201'
down_revision: Union[str, None] = 'fb416f7b214e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'task_comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False),
        sa.Column('employee_id', sa.Integer, sa.ForeignKey('employees.id', ondelete='SET NULL'), nullable=True),
        sa.Column('text', sa.Text),
    )


def downgrade() -> None:
    op.drop_table('task_comments')
