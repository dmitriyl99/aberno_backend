"""Create table sick leave

Revision ID: a32fa44c7b8b
Revises: 6a96272c4b18
Create Date: 2024-04-17 15:30:43.032315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a32fa44c7b8b'
down_revision: Union[str, None] = '6a96272c4b18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sick_leave',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('roll_call_id', sa.Integer, nullable=False),
        sa.Column('note', sa.String(200), nullable=True),
        sa.Column('date_from', sa.Date, nullable=False),
        sa.Column('date_to', sa.Date, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
        sa.ForeignKeyConstraint(['roll_call_id'], ['roll_calls.id'])
    )


def downgrade() -> None:
    op.drop_table('sick_leave')
