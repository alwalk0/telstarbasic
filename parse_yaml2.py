import yaml
from notes import notes, database
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn


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

app_routes = []

with open('config2.yml', 'r') as file:
    yaml_dict = yaml.safe_load(file)
    for key,value in yaml_dict.items():
        for k, v in value.items():
            print(v['method'])
            url = v['url']
            app_routes.append(Route(url, endpoint=eval(k), methods=[v['method']]))


app = Starlette(
    routes=app_routes,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect]
)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
    