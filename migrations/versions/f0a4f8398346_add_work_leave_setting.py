"""Add work leave setting

Revision ID: f0a4f8398346
Revises: a8bfe390b96b
Create Date: 2024-05-13 11:10:36.260764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f0a4f8398346'
down_revision: Union[str, None] = 'a8bfe390b96b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'organization_settings',
        sa.Column(
            'work_leave_enabled',
            sa.Boolean(),
            nullable=True,
            default=False)
    )


def downgrade() -> None:
    op.drop_column('organization_settings', 'work_leave_enabled')
