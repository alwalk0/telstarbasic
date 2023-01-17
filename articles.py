import databases
import sqlalchemy



DATABASE_URL = 'postgresql://newuser:postgres@localhost/test'


# Database table definitions.
metadata = sqlalchemy.MetaData()

articles = sqlalchemy.Table(
    "articles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("url", sqlalchemy.String),
)

database = databases.Database(DATABASE_URL)
