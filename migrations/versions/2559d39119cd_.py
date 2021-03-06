"""empty message

Revision ID: 2559d39119cd
Revises: 0c4fd8e1436d
Create Date: 2021-11-26 10:24:33.446980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2559d39119cd'
down_revision = '0c4fd8e1436d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chocolate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_location', sa.String(length=64), nullable=False),
    sa.Column('country_of_bean_origin', sa.String(length=64), nullable=False),
    sa.Column('company_location_id', sa.String(), nullable=True),
    sa.Column('country_of_bean_origin_id', sa.String(), nullable=True),
    sa.Column('cocoa_percent', sa.Float(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['company_location_id'], ['countries.country_name'], ),
    sa.ForeignKeyConstraint(['country_of_bean_origin_id'], ['countries.country_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chocolate')
    # ### end Alembic commands ###
