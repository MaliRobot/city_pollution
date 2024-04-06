"""so2 nullable in pollution

Revision ID: a5e5c8386a59
Revises: d61474be05a1
Create Date: 2024-04-06 01:04:56.175436

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a5e5c8386a59"
down_revision: Union[str, None] = "d61474be05a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "pollution",
        "so2",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "pollution",
        "so2",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    # ### end Alembic commands ###
