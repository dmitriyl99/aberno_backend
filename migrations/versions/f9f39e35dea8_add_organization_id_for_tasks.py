"""add organization id for tasks

Revision ID: f9f39e35dea8
Revises: 27413cf9731f
Create Date: 2024-05-07 21:42:28.481429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9f39e35dea8'
down_revision: Union[str, None] = '27413cf9731f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks',
                  sa.Column(
                      'organization_id',
                      sa.Integer(), sa.ForeignKey('organizations.id')))


def downgrade() -> None:
    op.drop_column('tasks', 'organization_id')
