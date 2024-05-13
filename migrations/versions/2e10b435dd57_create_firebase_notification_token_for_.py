"""create firebase notification token for users table

Revision ID: 2e10b435dd57
Revises: f0a4f8398346
Create Date: 2024-05-13 19:09:32.969312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e10b435dd57'
down_revision: Union[str, None] = 'f0a4f8398346'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('firebase_notification_token', sa.Text, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'firebase_notification_token')
