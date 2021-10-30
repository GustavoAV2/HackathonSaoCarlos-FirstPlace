"""empty message

Revision ID: 23517ca71e15
Revises: a3b21f637a4e
Create Date: 2021-10-30 15:00:54.796689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23517ca71e15'
down_revision = 'a3b21f637a4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=84), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
