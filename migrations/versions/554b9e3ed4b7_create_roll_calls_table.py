"""Create roll calls table

Revision ID: 554b9e3ed4b7
Revises: 4be4454d3548
Create Date: 2024-04-15 16:53:23.648359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '554b9e3ed4b7'
down_revision: Union[str, None] = '4be4454d3548'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('roll_calls',
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column('employee_id', sa.Integer(), nullable=False),
                    sa.Column('organization_id', sa.Integer(), nullable=False),
                    sa.Column('department_id', sa.Integer(), nullable=False),
                    sa.Column('status', sa.Enum('ON_WORK', 'OFF_DAY', 'SICK', 'REASONED'), nullable=False),
                    sa.Column('note', sa.String(200), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
                    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id']),
                    sa.ForeignKeyConstraint(['department_id'], ['departments.id']),
                    sa.PrimaryKeyConstraint("id"),
                    )


def downgrade() -> None:
    op.drop_table('roll_calls')
