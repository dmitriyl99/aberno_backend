"""Create tasks table

Revision ID: 4357df824632
Revises: 2db4a0e9385f
Create Date: 2024-05-04 17:17:51.269838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4357df824632'
down_revision: Union[str, None] = '2db4a0e9385f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status', sa.String(100), nullable=False),
        sa.Column('department_id',  sa.Integer, sa.ForeignKey('departments.id'), nullable=True),
        sa.Column('executor_id',  sa.Integer, sa.ForeignKey('employees.id'), nullable=True),
        sa.Column('priority', sa.String(50), nullable=True),
        sa.Column('deadline', sa.Date(), nullable=True),
        sa.Column('created_by_id', sa.Integer, sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('tasks')
