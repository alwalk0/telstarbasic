import yaml
from articles import articles, database
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from .create_view_function import create_function
   

get_request = create_function(table=articles, database=database)    


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