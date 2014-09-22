"""empty message

Revision ID: 4b24d5742f0e
Revises: 5717a31c1233
Create Date: 2014-09-16 16:46:30.133193

"""

# revision identifiers, used by Alembic.
revision = '4b24d5742f0e'
down_revision = '5717a31c1233'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'catalog_product', ['sku'])
    op.drop_constraint(u'state', 'sales_order')
    op.create_unique_constraint(None, 'sales_order', ['increment_id'])
    op.add_column('sales_order_item', sa.Column('row_weight', sa.Numeric(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sales_order_item', 'row_weight')
    op.drop_constraint(None, 'sales_order')
    op.create_unique_constraint(u'state', 'sales_order', ['state'])
    op.drop_constraint(None, 'catalog_product')
    ### end Alembic commands ###
