"""empty message

Revision ID: d6513a1581c7
Revises: 633a4113d28b
Create Date: 2021-11-24 09:32:06.927729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6513a1581c7'
down_revision = '633a4113d28b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country_drinks_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_name', sa.String(length=64), nullable=True),
    sa.Column('beer_servings', sa.Float(), nullable=True),
    sa.Column('spirit_servings', sa.Float(), nullable=True),
    sa.Column('wine_servings', sa.Float(), nullable=True),
    sa.Column('total_litres_of_pure_alcohol', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('country_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('country_drinks_info')
    # ### end Alembic commands ###
