"""add last few columns to post table

Revision ID: a7c881d436e8
Revises: 94cf01c289bf
Create Date: 2025-01-13 22:03:15.156560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7c881d436e8'
down_revision: Union[str, None] = '94cf01c289bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade():
    op.drop_column('posts', 'created_at')
    
