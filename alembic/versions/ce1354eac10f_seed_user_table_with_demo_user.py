"""seed_user_table_with_demo_user

Revision ID: ce1354eac10f
Revises: f118266bfee5
Create Date: 2022-02-17 06:10:55.709112

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import table, column, Integer, String

from app import bcrypt

revision = 'ce1354eac10f'
down_revision = 'f118266bfee5'
branch_labels = None
depends_on = None


def upgrade():
    user_table = table('users',
                       column('id', Integer),
                       column('name', String),
                       column('email', String),
                       column('password', String),
                       )

    op.bulk_insert(user_table, [
        {
            "name": "demo",
            "email": "demo@weatherapp.com",
            "password": bcrypt.generate_password_hash("password").decode('utf-8')
        }
    ])


def downgrade():
    pass
