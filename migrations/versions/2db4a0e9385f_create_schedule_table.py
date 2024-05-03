"""Create schedule table

Revision ID: 2db4a0e9385f
Revises: 015734dc9af3
Create Date: 2024-05-03 21:28:59.020664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2db4a0e9385f'
down_revision: Union[str, None] = '015734dc9af3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'schedules',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id'), nullable=False),
    )

    op.add_column(
        'departments',
        sa.Column(
            'schedule_id',
            sa.Integer,
            sa.ForeignKey('schedules.id'),
            nullable=True)
    )

    op.create_table(
        'schedule_days',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('day', sa.String(20), nullable=False),
        sa.Column('is_work_day', sa.Boolean, default=True),
        sa.Column('work_start_time', sa.String(5), nullable=True),
        sa.Column('work_end_time', sa.String(5), nullable=True),
        sa.Column('roll_call_start_time', sa.String(5), nullable=True),
        sa.Column('roll_call_end_time', sa.String(5), nullable=True),
        sa.Column('schedule_id', sa.Integer, sa.ForeignKey('schedules.id')),
    )


def downgrade() -> None:
    op.drop_column('departments', 'schedule_id')
    op.drop_table('schedule_days')
    op.drop_table('schedules')
