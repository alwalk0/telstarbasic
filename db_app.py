import databases
import sqlalchemy
from articles import articles, database
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn


#GET
async def list_notes(request):
    query = articles.select()
    results = await database.fetch_all(query)
    content = [
        {
            "title": result["title"],
            "url": result["url"]
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


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
    