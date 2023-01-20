
from starlette.responses import JSONResponse


def set_response(method, type, results):
    if type == 'json':
        if method == 'GET':
            content = [
            {
                "title": result["title"],
                "url": result["url"]
            }
            for result in results
            ]
            return JSONResponse(content)
        elif method == 'POST':
            return JSONResponse({'OK':'OK'})

    else:
        pass        

def get_query(input, table, data):
    if input == 'GET':
        return table.select()
    elif input == 'POST':
        
        return table.insert().values(
        title=data["title"],
        url=data["url"]
        )
    else:
        pass
    #TODO

def get_execute_function(input, database, query):
    if input == 'GET':
        return database.fetch_all(query)
    elif input == 'POST':
        return database.execute(query)



def create_function(table, database, method, *args, **kwargs):

    async def function_template(request, *args, **kwargs):

        if method == 'POST':
            
            data = await request.json()
            query = get_query(method, table, data)
        else:
            query = get_query(method, table, data=None)   

        results = await get_execute_function(method, database, query)

        return set_response(method, 'json', results)

    return function_template 