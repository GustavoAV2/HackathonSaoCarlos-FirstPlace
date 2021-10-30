"""empty message

Revision ID: 79b6694dcd3f
Revises: e9969c823086
Create Date: 2021-10-30 13:23:31.213062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79b6694dcd3f'
down_revision = 'e9969c823086'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('email', sa.VARCHAR(length=84), nullable=False),
    sa.Column('password', sa.VARCHAR(length=128), nullable=True),
    sa.Column('active', sa.BOOLEAN(), nullable=True),
    sa.CheckConstraint('active IN (0, 1)'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_table('groups')
    # ### end Alembic commands ###
