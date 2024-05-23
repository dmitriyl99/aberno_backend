"""change employee position

Revision ID: bc1a703be576
Revises: b7241a3f0f6b
Create Date: 2024-05-23 17:04:55.364859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc1a703be576'
down_revision: Union[str, None] = 'b7241a3f0f6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('employees', 'position')
    op.add_column('employees', sa.Column('position_id', sa.Integer, sa.ForeignKey('positions.id')))


def downgrade() -> None:
    op.add_column('employees', sa.Column('position', sa.String(200), nullable=True))
    op.drop_column('employees', 'position_id')
