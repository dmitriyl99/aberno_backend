"""Add employee number for user

Revision ID: 10677fb1c23c
Revises: cee1d64dfea7
Create Date: 2024-05-28 22:24:36.679893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10677fb1c23c'
down_revision: Union[str, None] = 'cee1d64dfea7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("employee_number", sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'employee_number')
