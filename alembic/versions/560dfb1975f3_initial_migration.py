"""Initial migration

Revision ID: 560dfb1975f3
Revises: c2b2dbca5d3d
Create Date: 2025-01-18 19:21:32.592513

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "560dfb1975f3"
down_revision: Union[str, None] = "c2b2dbca5d3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("xlsx_data", sa.Column("open", sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("xlsx_data", "open")
    # ### end Alembic commands ###
