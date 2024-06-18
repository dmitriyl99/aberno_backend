"""add controller to tasks table

Revision ID: fb416f7b214e
Revises: 9beef79ebe3f
Create Date: 2024-06-18 22:51:28.467055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb416f7b214e'
down_revision: Union[str, None] = '9beef79ebe3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'tasks',
        sa.Column(
            'controller_employee_id',
            sa.Integer(),
            sa.ForeignKey(
                'employees.id',
                ondelete='SET NULL'
            ),
            nullable=True
        )
    )


def downgrade() -> None:
    op.drop_column('tasks', 'controller_employee_id')
