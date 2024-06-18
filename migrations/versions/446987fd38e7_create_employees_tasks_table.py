"""create employees_tasks_table

Revision ID: 446987fd38e7
Revises: bc1a703be576
Create Date: 2024-06-14 10:42:54.213880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '446987fd38e7'
down_revision: Union[str, None] = 'bc1a703be576'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'employees_tasks',
        sa.Column('employee_id', sa.Integer, sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id'), nullable=False),
        sa.Column('status', sa.String(100), nullable=False),
        sa.Column('viewed', sa.Boolean, default=False),
        sa.Column('viewed_at', sa.DateTime, nullable=True)
    )
    op.drop_column('tasks', 'executor_id')
    op.drop_column('tasks', 'viewed')
    op.drop_column('tasks', 'viewed_at')


def downgrade() -> None:
    op.drop_table('employees_tasks')
    op.add_column('tasks',
                  sa.Column(
                      'executor_id',
                      sa.Integer,
                      sa.ForeignKey('employees.id'),
                      nullable=True)
                  )
    op.add_column('tasks',
                  sa.Column(
                      'viewed',
                      sa.Boolean,
                      default=False)
                  )
    op.add_column('tasks',
                  sa.Column(
                      'viewed_at',
                      sa.DateTime,
                      nullable=True)
                  )
