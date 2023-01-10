"""Create notes table

Revision ID: 9d43c36729d5
Revises: 
Create Date: 2023-01-09 18:33:52.570546

"""
from alembic import op
import sqlalchemy


# revision identifiers, used by Alembic.
revision = '9d43c36729d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'notes',
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("text", sqlalchemy.String),
        sqlalchemy.Column("completed", sqlalchemy.Boolean),
    )


def downgrade() -> None:
    op.drop_table('notes')
