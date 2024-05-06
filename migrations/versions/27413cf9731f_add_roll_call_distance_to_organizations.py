"""Add roll call distance to organizations

Revision ID: 27413cf9731f
Revises: 4357df824632
Create Date: 2024-05-06 10:18:37.170785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27413cf9731f'
down_revision: Union[str, None] = '4357df824632'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('organization_settings',
                  sa.Column('roll_call_distance', sa.Integer, default=200))


def downgrade() -> None:
    op.drop_column('organization_settings', 'roll_call_distance')
