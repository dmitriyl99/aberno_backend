"""create organization settings table

Revision ID: ff44cf9f3a31
Revises: a32fa44c7b8b
Create Date: 2024-04-29 14:10:11.067129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import time


# revision identifiers, used by Alembic.
revision: str = 'ff44cf9f3a31'
down_revision: Union[str, None] = 'a32fa44c7b8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'organization_settings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('organization_id', sa.Integer, sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('roll_call_start_time', sa.String(5)),
        sa.Column('roll_call_end_time', sa.String(5)),
    )


def downgrade() -> None:
    op.drop_table('organization_settings')
