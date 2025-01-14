"""add published column to posts table

Revision ID: 5ef79bbaade7
Revises: e0d34095b2e0
Create Date: 2025-01-13 21:40:11.268967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ef79bbaade7'
down_revision: Union[str, None] = 'e0d34095b2e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean, server_default="TRUE", nullable=False))
    


def downgrade():
    op.drop_column("posts", "published")
    