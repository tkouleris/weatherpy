"""create_pivot_table_user_city

Revision ID: da70323730e6
Revises: ce1354eac10f
Create Date: 2022-02-21 05:52:35.952346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import table, column, Integer

revision = 'da70323730e6'
down_revision = 'ce1354eac10f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'city_user',
        sa.Column('city_id', sa.Integer, sa.ForeignKey('city.id')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'))
    )

    pivot_table = table('city_user',
                       column('city_id', Integer),
                       column('user_id', Integer),
                       )

    op.bulk_insert(pivot_table, [
        {
            "city_id": 2656,
            "user_id": 1,
        },
        {
            "city_id": 19583,
            "user_id": 1,
        }
    ])


def downgrade():
    op.drop_table('city_user')
