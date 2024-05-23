"""create positions table

Revision ID: b7241a3f0f6b
Revises: 466782bf0aa3
Create Date: 2024-05-23 16:16:47.323766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7241a3f0f6b'
down_revision: Union[str, None] = '466782bf0aa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200)),
        sa.Column('organization_id', sa.Integer, sa.ForeignKey('organizations.id')),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('positions')

