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
from starlette.requests import Request

request = Request


def create_function(table, *args, **kwargs):

    async def function_template(*args, **kwargs):

        query = table.select()
        results = await database.fetch_all(query)
        content = [
            {
                "text": result["text"],
                "completed": result["completed"]
            }
            for result in results
        ]
        return JSONResponse(content)

    return function_template    

get_request = create_function(table=notes)    


def create_app_from_config(config):

    app_routes = []

    with open(config, 'r') as file:
        yaml_dict = yaml.safe_load(file)
        for key,value in yaml_dict.items():
            for k, v in value.items():
                print(v['db_table'])
                url = v['url']
                app_routes.append(Route(url, endpoint=get_request, methods=[v['method']]))


    app = Starlette(
        routes=app_routes,
        on_startup=[database.connect],
        on_shutdown=[database.disconnect]
    )

    return app