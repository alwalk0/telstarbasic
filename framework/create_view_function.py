
from starlette.responses import JSONResponse


#GET
async def list_notes(request):
    query = articles.select()
    results = await database.fetch_all(query)
    content = [
        {
            "text": result["text"],
            "completed": result["completed"]
        }
        for result in results
    ]
    return JSONResponse(content)

#POST
async def add_note(request):
    data = await request.json()
    query = articles.insert().values(
       text=data["text"],
       completed=data["completed"]
    )
    await database.execute(query)
    return JSONResponse({
        "text": data["text"],
        "completed": data["completed"]
    })


def set_response(input, data):
    if input == 'json':
        return JSONResponse({'ok': 'ok'})
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



def create_function(table, database, *args, **kwargs):

    async def function_template(request, *args, **kwargs):

        data = await request.json()

        query = get_query('POST', table, data)
        results = await get_execute_function('POST', database, query)
        content = [
            {
                "title": result["title"],
                "url": result["url"]
            }
            for result in results
        ]
        return JSONResponse({'ok': 'ok'})

    return function_template 