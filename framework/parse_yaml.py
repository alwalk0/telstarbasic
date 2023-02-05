import yaml
from articles import articles
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
import importlib
import importlib.machinery
from pathlib import Path
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from databases import Database
from starlette.requests import Request


def set_response(method: str, type, results, fields):
    match type:
        case 'json':
            match method:
                case 'GET':
                    content = [
                    {
                        field: result[field] for field in fields
                    }
                    for result in results
                    ]
                    return JSONResponse(content)
                case 'POST':
                    return JSONResponse({'OK':'OK'})
            

async def get_query(request: Request, method: str, table):
    match method:
        case 'GET':
            return table.select()
        case 'POST':
            data = await request.json()
            return table.insert().values(data)


def get_execute_function(method: str, query, database: Database):

    match method:
        case 'GET':
            return database.fetch_all(query)
        case 'POST':
            return database.execute(query)


def create_view_function(specs:dict, database: Database) -> callable:

    method = specs['method']
    return_type = specs['return']
    fields = (specs['fields']).split(', ')
    table = specs['db_table']

    async def view_function(request):

        query = await get_query(request, method=method, table=eval(table))

        results = await get_execute_function(method=method, query=query, database=database)

        return set_response(method=method, type=return_type, results=results, fields=fields)

    return view_function 


def read_key_from_config(config:str, key:str)-> str:
    with open(config, 'r') as file:
        yaml_dict = yaml.safe_load(file)
    
    return yaml_dict.get(key)


def get_database(models:str, database:str) -> Database:

    module_path = Path(__file__).parent.parent
    file_path = str(module_path) + '/' + models
    modulename = importlib.machinery.SourceFileLoader(models.removesuffix('.py'), file_path).load_module()

    return getattr(modulename, database)
    

def create_routes_list(yaml_dict: dict, database: Database, templates: Jinja2Templates) -> list:
    app_routes = []

    for view, specs in yaml_dict.items():
        endpoint = specs['endpoint']
        url = specs['url']
        if endpoint == 'api':
                
            method = specs['method']
            app_routes.append(Route(url, endpoint=create_view_function(specs=specs, database=database),methods=[method]))

        elif endpoint == 'view':
            template = specs['template']
            app_routes.append(Route(url, lambda request:templates.TemplateResponse(template, {'request':request})))
            app_routes.append(Mount('/static', app=StaticFiles(directory='statics'), name='static'))     

    return app_routes      


def create_app_from_config(main_config:str)-> Starlette:

    views_config = main_config['views']
    models = main_config['models']
    database = main_config['database']
    templates = main_config['templates']

    with open(views_config, 'r') as file:
        views_dict = yaml.safe_load(file)    

    database = get_database(models, database)

    templates = Jinja2Templates(directory=str(templates))

    app_routes = create_routes_list(yaml_dict=views_dict, database=database, templates=templates)    

    app = Starlette(
        routes=app_routes,
        on_startup=[database.connect],
        on_shutdown=[database.disconnect]
    )

    return app


