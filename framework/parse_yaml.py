import yaml
from articles import articles, database
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Route
from .create_view_function import create_view_function
   

def create_app_from_config(config):

    app_routes = []

    with open(config, 'r') as file:
        yaml_dict = yaml.safe_load(file)
        for key,value in yaml_dict.items():
            for k, v in value.items():
                url = v['url']
                method = v['method']
                db_table = v['db_table']
                return_type = v['return']
                fields = (v['fields']).split(', ')

                app_routes.append(Route(url, endpoint=create_view_function(table=articles, database=database, method=method, return_type=return_type, fields=fields),methods=[method]))


    app = Starlette(
        routes=app_routes,
        on_startup=[database.connect],
        on_shutdown=[database.disconnect]
    )

    return app