import yaml
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
import uvicorn



templates = Jinja2Templates(directory='templates')


app_routes = []

with open('config.yml', 'r') as file:
    yaml_dict = yaml.safe_load(file)

    for key,value in yaml_dict.items():
        for k, v in value.items():
            url = v['url']
            template = v['template']
            print(url)
            print(template)
            app_routes.append(Route(url, lambda request:templates.TemplateResponse(template, {'request':request})))



app_routes.append(Mount('/static', app=StaticFiles(directory='statics'), name='static'))   


# routes = [
#     Route('/', lambda request:templates.TemplateResponse("index.html", {'request':request})),
#     Route('/error', error),
#     Mount('/static', app=StaticFiles(directory='statics'), name='static')
# ]



app = Starlette(debug=True, routes=app_routes)    



if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
    