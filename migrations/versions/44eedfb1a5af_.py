"""empty message

Revision ID: 44eedfb1a5af
Revises: 
Create Date: 2021-10-30 19:42:38.484184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44eedfb1a5af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('first_name', sa.String(length=150), nullable=False),
    sa.Column('last_name', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=84), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=150), nullable=False),
    sa.Column('cep', sa.String(length=10), nullable=False),
    sa.Column('cpf_or_cnpj', sa.String(length=16), nullable=False),
    sa.Column('rg', sa.String(length=20), nullable=False),
    sa.Column('legal_person', sa.Boolean(), nullable=True),
    sa.Column('birth_file', sa.String(length=200), nullable=False),
    sa.Column('wedding_file', sa.String(length=200), nullable=False),
    sa.Column('residence_file', sa.String(length=200), nullable=False),
    sa.Column('income_tax_file', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address'),
    sa.UniqueConstraint('birth_file'),
    sa.UniqueConstraint('cep'),
    sa.UniqueConstraint('cpf_or_cnpj'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('first_name'),
    sa.UniqueConstraint('income_tax_file'),
    sa.UniqueConstraint('last_name'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('residence_file'),
    sa.UniqueConstraint('rg'),
    sa.UniqueConstraint('wedding_file')
    )
    op.create_table('groups',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
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
    op.drop_table('groups')
    op.drop_table('clients')
    # ### end Alembic commands ###
