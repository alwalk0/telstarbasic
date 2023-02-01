import yaml
from articles import articles
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from .create_view_function import create_view_function
import importlib
import importlib.machinery
from pathlib import Path


module_path = Path(__file__).parent.parent
modulename = importlib.machinery.SourceFileLoader('articles', '/Users/alan/Desktop/Projects/Code/telstarbasic/articles.py').load_module()
module = getattr(modulename, 'database')
print(module)



templates = Jinja2Templates(directory='templates')


def create_routes_list(database, yaml_dict: dict) -> list:
    app_routes = []
    for key,value in yaml_dict.items():
        for k, v in value.items():
            endpoint = v['endpoint']
            url = v['url']
            if endpoint == 'api':
                    
                method = v['method']
                db_table = v['db_table']
                return_type = v['return']
                fields = (v['fields']).split(', ')

                app_routes.append(Route(url, endpoint=create_view_function(table=eval(db_table), database=database, method=method, return_type=return_type, fields=fields),methods=[method]))

            elif endpoint == 'view':
                template = v['template']
                app_routes.append(Route(url, lambda request:templates.TemplateResponse(template, {'request':request})))
                app_routes.append(Mount('/static', app=StaticFiles(directory='statics'), name='static'))     

    return app_routes      


def create_app_from_config(config:str, models, templates, views)-> Starlette:

    with open(config, 'r') as file:
        yaml_dict = yaml.safe_load(file)

    database = getattr(modulename, 'database')    

    app_routes = create_routes_list(database, yaml_dict=yaml_dict)    

    app = Starlette(
        routes=app_routes,
        on_startup=[database.connect],
        on_shutdown=[database.disconnect]
    )

    return app


def parse_main_config(config:str):

    with open(config, 'r') as file:
        yaml_dict = yaml.safe_load(file)
        port = yaml_dict.get('port')
        host = yaml_dict.get('host')
        models = yaml_dict['apps']['models']
        templates = yaml_dict['apps']['templates']
        views = yaml_dict['apps']['views']
        database = yaml_dict['apps']['database']

        return port, host, models, templates, views, database

