"""Create roll call location table

Revision ID: 6a96272c4b18
Revises: 554b9e3ed4b7
Create Date: 2024-04-15 17:01:10.183063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6a96272c4b18'
down_revision: Union[str, None] = '554b9e3ed4b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("locations",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("lat", sa.Float(), nullable=False),
                    sa.Column("lng", sa.Float(), nullable=False),
                    sa.Column("roll_call_id", sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(["roll_call_id"], ["roll_calls.id"]),
                    sa.PrimaryKeyConstraint("id"),
                    )


def downgrade() -> None:
    op.drop_table("locations")
