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


def set_response(method, type, results, fields):
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
            

async def get_query(request, method, table):
    match method:
        case 'GET':
            return table.select()
        case 'POST':
            data = await request.json()
            return table.insert().values(data)


def get_execute_function(method, query, database):

    match method:
        case 'GET':
            return database.fetch_all(query)
        case 'POST':
            return database.execute(query)


def create_view_function(endpoint, database, templates, models):

    method = endpoint['method']
    return_type = endpoint['return']
    fields = (endpoint['fields']).split(', ')
    table = str(models).removesuffix('.py')

    async def view_function(request):

        query = await get_query(request, method, table=eval(table))

        results = await get_execute_function(method, query, database)

        return set_response(method, return_type, results, fields=fields)

    return view_function 


def read_key_from_config(config:str, key:str)-> str:
    with open(config, 'r') as file:
        yaml_dict = yaml.safe_load(file)
    
    return yaml_dict.get(key)


def get_database(models, database):

    module_path = Path(__file__).parent.parent
    file_path = str(module_path) + '/' + models
    modulename = importlib.machinery.SourceFileLoader(models.removesuffix('.py'), file_path).load_module()

    return getattr(modulename, database)
    

def create_routes_list(yaml_dict: dict, database, templates, models) -> list:
    app_routes = []
    for key,value in yaml_dict.items():
        for k, v in value.items():
            endpoint = v['endpoint']
            url = v['url']
            if endpoint == 'api':
                    
                method = v['method']

                app_routes.append(Route(url, endpoint=create_view_function(v, database, templates, models),methods=[method]))

            elif endpoint == 'view':
                template = v['template']
                app_routes.append(Route(url, lambda request:templates.TemplateResponse(template, {'request':request})))
                app_routes.append(Mount('/static', app=StaticFiles(directory='statics'), name='static'))     

    return app_routes      


def create_app_from_config(config:str)-> Starlette:

    with open(config, 'r') as file:
        main_config = yaml.safe_load(file)

    views_config = main_config['views']

    with open(views_config, 'r') as file:
        views_dict = yaml.safe_load(file)    

    database = get_database(main_config['models'], main_config['database'])

    templates = Jinja2Templates(directory=str(main_config['templates']))

    app_routes = create_routes_list(yaml_dict=views_dict, database=database, templates=templates, models=main_config['models'])    

    app = Starlette(
        routes=app_routes,
        on_startup=[database.connect],
        on_shutdown=[database.disconnect]
    )

    return app


