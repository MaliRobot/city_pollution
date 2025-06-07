"""make_state_optional

Revision ID: 2a3b4c5d6e7f
Revises: c900f94761b0
Create Date: 2025-06-07 19:18:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2a3b4c5d6e7f"
down_revision: Union[str, None] = "c900f94761b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make state column nullable
    op.alter_column("city", "state", existing_type=sa.String(255), nullable=True)


def downgrade() -> None:
    # Make state column non-nullable again
    op.alter_column("city", "state", existing_type=sa.String(255), nullable=False)
