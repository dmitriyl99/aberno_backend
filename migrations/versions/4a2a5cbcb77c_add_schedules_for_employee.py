"""add schedules for employee

Revision ID: 4a2a5cbcb77c
Revises: b91781de7e75
Create Date: 2024-07-30 10:06:21.252377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a2a5cbcb77c'
down_revision: Union[str, None] = 'b91781de7e75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'schedules',
        sa.Column(
            'employee_id',
            sa.Integer(),
            sa.ForeignKey(
                'employees.id',
                ondelete='CASCADE'
            ),
            nullable=True
        )
    )
    op.alter_column('schedules', 'department_id', nullable=True)
    op.add_column('employees', sa.Column('schedule_type', sa.String(50), default='ORGANIZATION'))


def downgrade() -> None:
    op.drop_column('schedules', 'employee_id')
    op.drop_column('employees', 'schedule_type')
