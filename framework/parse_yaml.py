import yaml
from articles import articles, database
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from .create_view_function import create_view_function

templates = Jinja2Templates(directory='templates')

   

def create_app_from_config(config):

    app_routes = []

    with open(config, 'r') as file:
        yaml_dict = yaml.safe_load(file)
        for key,value in yaml_dict.items():
            for k, v in value.items():
                endpoint = v['endpoint']
                url = v['url']
                if endpoint == 'api':
                        
                    method = v['method']
                    db_table = v['db_table']
                    return_type = v['return']
                    fields = (v['fields']).split(', ')

                    app_routes.append(Route(url, endpoint=create_view_function(table=articles, database=database, method=method, return_type=return_type, fields=fields),methods=[method]))

                elif endpoint == 'view':
                    template = v['template']
                    app_routes.append(Route(url, lambda request:templates.TemplateResponse(template, {'request':request})))
                    app_routes.append(Mount('/static', app=StaticFiles(directory='statics'), name='static'))        
  


    app = Starlette(
        routes=app_routes,
        on_startup=[database.connect],
        on_shutdown=[database.disconnect]
    )

    return app