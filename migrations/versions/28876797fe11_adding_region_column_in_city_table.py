"""Adding region column in city table

Revision ID: 28876797fe11
Revises: 7ed76ec3c89f
Create Date: 2023-07-16 18:19:15.046682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28876797fe11'
down_revision = '7ed76ec3c89f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('city', schema=None) as batch_op:
        batch_op.add_column(sa.Column('region', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('city', schema=None) as batch_op:
        batch_op.drop_column('region')

    # ### end Alembic commands ###
