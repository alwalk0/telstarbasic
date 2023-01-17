"""create articles table

Revision ID: e059b11c09e3
Revises: 
Create Date: 2023-01-17 01:41:00.052794

"""
from alembic import op
import sqlalchemy 


# revision identifiers, used by Alembic.
revision = 'e059b11c09e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('articles',
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("url", sqlalchemy.String),
)


def downgrade():
    op.drop_table('articles')
