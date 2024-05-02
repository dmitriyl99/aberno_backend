"""add created by to employees table


Revision ID: 6ed544830b63
Revises: 0fc25fbb142c
Create Date: 2024-05-02 11:08:24.616321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ed544830b63'
down_revision: Union[str, None] = '0fc25fbb142c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('employees', sa.Column('created_by_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True))


def downgrade() -> None:
    op.drop_column('employees', 'created_by_id')
