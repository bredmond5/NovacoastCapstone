"""empty message

Revision ID: 1f3a79c46f75
Revises: c4191feb177a
Create Date: 2020-09-24 15:31:46.852046

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1f3a79c46f75'
down_revision = 'c4191feb177a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('domain', 'updated_at')
    op.add_column('domain', sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))


def downgrade():
    op.drop_column('domain', 'updated_at')
    op.add_column('domain', sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
