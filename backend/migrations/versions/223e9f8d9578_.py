"""empty message

Revision ID: 223e9f8d9578
Revises: 
Create Date: 2020-09-03 11:09:39.173826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '223e9f8d9578'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emails', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('last_emailed', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), server_default='', nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('domain')
    op.drop_table('group')
    # ### end Alembic commands ###
