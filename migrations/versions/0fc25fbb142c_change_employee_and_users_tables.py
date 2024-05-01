"""Change employee and users tables

Revision ID: 0fc25fbb142c
Revises: ff44cf9f3a31
Create Date: 2024-05-01 14:00:42.519853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fc25fbb142c'
down_revision: Union[str, None] = 'ff44cf9f3a31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('last_name', sa.String(200), nullable=True))
    op.add_column('employees', sa.Column('position', sa.String(200), nullable=True))
    op.drop_column('employees', 'birth_date')


def downgrade() -> None:
    op.drop_column('users', 'last_name')
    op.drop_column('employees', 'position')
    op.add_column('employees', sa.Column('birth_date', sa.Date, nullable=True))
