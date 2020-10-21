"""empty message

Revision ID: e9274bd73b13
Revises: 812830621432
Create Date: 2020-09-21 13:20:17.958533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9274bd73b13'
down_revision = '812830621432'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('domain', sa.Column('scan_period', sa.Integer(), nullable=True))
    op.execute('UPDATE domain SET scan_period=24;')
    op.alter_column('domain', 'scan_period', nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('domain', 'scan_period')
    # ### end Alembic commands ###