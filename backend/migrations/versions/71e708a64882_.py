"""empty message

Revision ID: 71e708a64882
Revises: 1f3a79c46f75
Create Date: 2020-10-20 13:06:11.044524

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '71e708a64882'
down_revision = '1f3a79c46f75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('domain', 'time_zone')
    op.drop_column('domain', 'recur')
    op.drop_column('domain', 'start_at')
    op.add_column('group', sa.Column('recur', sa.String(), server_default='daily', nullable=False))
    op.add_column('group', sa.Column('start_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('group', sa.Column('time_zone', sa.String(), server_default='UTC', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'time_zone')
    op.drop_column('group', 'start_at')
    op.drop_column('group', 'recur')
    op.add_column('domain', sa.Column('start_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.add_column('domain', sa.Column('recur', sa.VARCHAR(), server_default=sa.text("'daily'::character varying"), autoincrement=False, nullable=False))
    op.add_column('domain', sa.Column('time_zone', sa.VARCHAR(), server_default=sa.text("'UTC'::character varying"), autoincrement=False, nullable=False))
    # ### end Alembic commands ###