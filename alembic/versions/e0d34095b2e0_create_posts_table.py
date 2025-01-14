"""create posts table

Revision ID: e0d34095b2e0
Revises: 
Create Date: 2025-01-13 21:27:39.497031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0d34095b2e0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# https://alembic.sqlalchemy.org/en/latest/api/ddl.html
def upgrade():
    op.create_table(
        "posts", 
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False)
                     )


def downgrade():
    op.drop_table("posts")
