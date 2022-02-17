"""create_city_table

Revision ID: f118266bfee5
Revises: a62e5b624da4
Create Date: 2022-02-14 06:02:15.810320

"""
import json
import os

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import table, column, Integer, String

revision = 'f118266bfee5'
down_revision = 'a62e5b624da4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'city',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('city', sa.String(255), nullable=False),
        sa.Column('city_state', sa.String(255), nullable=False),
        sa.Column('country', sa.String(255), nullable=False),
        sa.Column('owm_id', sa.Integer, nullable=False),
    )

    city_table = table('city',
                       column('id', Integer),
                       column('city', String),
                       column('city_state', String),
                       column('country', String),
                       column('owm_id', Integer)
                       )

    file = os.path.dirname(os.path.realpath(__file__)) + "\\..\\data\\city.list.json"
    f = open(file, encoding="utf8")
    cities = json.load(f)
    data_to_import = []
    for city in cities:
        single_city = {"city": city['name'], "city_state": city['state'], "country": city['country'],
                       "owm_id": city['id']}
        data_to_import.append(single_city)
    f.close()

    op.bulk_insert(city_table, data_to_import)


def downgrade():
    op.drop_table('city')
