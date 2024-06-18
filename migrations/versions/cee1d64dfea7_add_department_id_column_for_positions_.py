"""Add department id column for positions table

Revision ID: cee1d64dfea7
Revises: bc1a703be576
Create Date: 2024-05-28 19:50:09.700043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cee1d64dfea7'
down_revision: Union[str, None] = 'bc1a703be576'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('positions', sa.Column('department_id', sa.Integer(), sa.ForeignKey('departments.id'), nullable=True))


def downgrade() -> None:
    op.drop_column('positions', 'department_id')
