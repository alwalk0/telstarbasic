import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

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


# Main application code.
async def list_notes(request):
    query = notes.select()
    results = await database.fetch_all(query)
    content = [
        {
            "text": result["text"],
            "completed": result["completed"]
        }
        for result in results
    ]
    return JSONResponse(content)

async def add_note(request):
    data = await request.json()
    query = notes.insert().values(
       text=data["text"],
       completed=data["completed"]
    )
    await database.execute(query)
    return JSONResponse({
        "text": data["text"],
        "completed": data["completed"]
    })

routes = [
    Route("/notes", endpoint=list_notes, methods=["GET"]),
    Route("/notes", endpoint=add_note, methods=["POST"]),
]
 
app = Starlette(
    routes=routes,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect]
)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
    