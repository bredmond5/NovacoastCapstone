"""empty message

Revision ID: 42ea8cfe44dd
Revises: e9274bd73b13
Create Date: 2020-09-23 15:20:01.668230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42ea8cfe44dd'
down_revision = 'e9274bd73b13'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('domain', sa.Column('recur', sa.String(),
                                      server_default='daily', nullable=False))
    op.alter_column('domain', 'recur', nullable=False)
    op.add_column('domain', sa.Column('start_date', sa.DateTime(),
                                      server_default=sa.text('now()'),
                                      nullable=False))
    op.add_column('domain', sa.Column('time_zone', sa.String(),
                                      server_default='UTC', nullable=False))
    op.drop_column('domain', 'scan_period')


def downgrade():
    op.add_column('domain', sa.Column('scan_period', sa.INTEGER(),
                                      autoincrement=False, nullable=False))
    op.drop_column('domain', 'time_zone')
    op.drop_column('domain', 'start_date')
    op.drop_column('domain', 'recur')
