import databases
import sqlalchemy

# Configuration from environment variables or '.env' file.
# config = Config('.env')
DATABASE_URL = 'postgresql://newuser:postgres@localhost/test'


# Database table definitions.
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

database = databases.Database(DATABASE_URL)
