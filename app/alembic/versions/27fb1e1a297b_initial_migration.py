"""Initial migration

Revision ID: 27fb1e1a297b
Revises: 
Create Date: 2024-04-05 21:29:02.666251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27fb1e1a297b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('state', sa.String(length=255), nullable=False),
    sa.Column('country', sa.String(length=255), nullable=False),
    sa.Column('county', sa.String(length=255), nullable=True),
    sa.Column('lan', sa.Float(), nullable=False),
    sa.Column('lon', sa.Float(), nullable=False),
    sa.Column('time_created', sa.Integer(), nullable=True),
    sa.Column('time_updated', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pollution',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('co', sa.Float(), nullable=False),
    sa.Column('no', sa.Float(), nullable=False),
    sa.Column('no2', sa.Float(), nullable=False),
    sa.Column('o3', sa.Float(), nullable=False),
    sa.Column('so2', sa.Float(), nullable=False),
    sa.Column('pm2_5', sa.Float(), nullable=True),
    sa.Column('pm10', sa.Float(), nullable=True),
    sa.Column('nh3', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pollution')
    op.drop_table('city')
    # ### end Alembic commands ###
