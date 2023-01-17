import databases
import sqlalchemy
from articles import articles, database
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route


#GET
async def list_notes(request):
    query = articles.select()
    results = await database.fetch_all(query)
    content = [
        {
            "text": result["text"],
            "completed": result["completed"]
        }
        for result in results
    ]
    return JSONResponse(content)

#POST
async def add_note(request):
    data = await request.json()
    query = articles.insert().values(
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
