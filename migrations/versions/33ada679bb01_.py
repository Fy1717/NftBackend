"""empty message

Revision ID: 33ada679bb01
Revises: 
Create Date: 2022-05-16 23:22:58.995223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33ada679bb01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('admin', 'mod',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('ecommerce_admin', 'admin', type_='unique')
    op.create_unique_constraint(None, 'admin', ['name'])
    op.add_column('product', sa.Column('stock', sa.Integer(), nullable=False))
    op.alter_column('product', 'image',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.drop_constraint('ecommerce_user', 'user', type_='unique')
    op.create_unique_constraint(None, 'user', ['email'])
    op.create_unique_constraint(None, 'user', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.create_unique_constraint('ecommerce_user', 'user', ['username', 'email'])
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('product', 'image',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('product', 'stock')
    op.drop_constraint(None, 'admin', type_='unique')
    op.create_unique_constraint('ecommerce_admin', 'admin', ['name', 'email'])
    op.alter_column('admin', 'mod',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
