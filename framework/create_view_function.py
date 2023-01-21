
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
      

async def get_query(request, input, table):
    if input == 'GET':
        return table.select()
    if input == 'POST':
        data = await request.json()
        return table.insert().values(
        title=data["title"],
        url=data["url"]
        )


def get_execute_function(input, database, query):
    if input == 'GET':
        return database.fetch_all(query)
    elif input == 'POST':
        return database.execute(query)



def create_view_function(table, database, method):

    async def view_function(request):

        query = await get_query(request, method, table)
        results = await get_execute_function(method, database, query)

        return set_response(method, 'json', results)

    return view_function 