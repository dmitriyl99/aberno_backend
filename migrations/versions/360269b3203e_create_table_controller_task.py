"""create table controller_task

Revision ID: 360269b3203e
Revises: dbc672828201
Create Date: 2024-06-20 21:37:35.076672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '360269b3203e'
down_revision: Union[str, None] = 'dbc672828201'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'controller_task',
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id', ondelete='CASCADE')),
        sa.Column('employee_id', sa.Integer, sa.ForeignKey('employees.id', ondelete='CASCADE'))
    )
    op.drop_column('tasks', 'controller_employee_id')


def downgrade() -> None:
    op.drop_table('controller_task')
    op.add_column(
        'tasks',
        sa.Column(
            'controller_employee_id',
            sa.Integer(),
            sa.ForeignKey(
                'employees.id',
                ondelete='SET NULL'
            ),
            nullable=True
        )
    )
