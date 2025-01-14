"""add foreign key to posts table

Revision ID: 94cf01c289bf
Revises: 2b502f847256
Create Date: 2025-01-13 21:55:48.717522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94cf01c289bf'
down_revision: Union[str, None] = '2b502f847256'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('fk_posts_users', source_table='posts', referent_table='users', local_cols=['owner_id'],remote_cols= ['id'], ondelete='CASCADE')
    


def downgrade() -> None:
    op.drop_constraint('fk_posts_users', table_name= 'posts')
    op.drop_column('posts', 'owner_id')
    
