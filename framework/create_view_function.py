
from starlette.responses import JSONResponse



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


def get_execute_function(method, query):
    database = get_database()
    match method:
        case 'GET':
            return database.fetch_all(query)
        case 'POST':
            return database.execute(query)



def create_view_function(table, method, return_type, fields):

    async def view_function(request):

        query = await get_query(request, method, table)
        results = await get_execute_function(method, query)

        return set_response(method, return_type, results, fields=fields)

    return view_function 