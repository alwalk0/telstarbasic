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
import uvicorn


# # Main application code.
# async def get_request(request, table, fields):
#     query = table.select()
#     results = await database.fetch_all(query)
#     content = [
#         {
#             field: result[field] for field in fields
#         }
#         for result in results
#     ]
#     return JSONResponse(content)

# async def post_request(request, table, fields):
#     data = await request.json()
#     query = ot.insert().values(
#        text=data["text"],
#        completed=data["completed"]
#     )
#     await database.execute(query)
#     return JSONResponse({
#         "text": data["text"],
#         "completed": data["completed"]
#     })


table = notes
request = Request


###############################################################################    


# def construct_query(table, fields):
#     if request_get:
#         query = table.select()
#     if request_post:
#         table.insert().values(fields) 
     

# def create_function(query, *args, **kwargs):

#     async def function_template(*args, **kwargs):

#         query = table.select()
#         results = await database.fetch_all(query)
#         content = [
#             {
#                 "text": result["text"],
#                 "completed": result["completed"]
#             }
#             for result in results
#         ]
#         return JSONResponse(content)

#     return function_template    



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


app_routes = []

with open('config2.yml', 'r') as file:
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

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
    