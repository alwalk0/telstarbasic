
from starlette.responses import JSONResponse



def create_function(table, database, *args, **kwargs):

    async def function_template(*args, **kwargs):

        query = table.select()
        results = await database.fetch_all(query)
        content = [
            {
                "title": result["title"],
                "url": result["url"]
            }
            for result in results
        ]
        return JSONResponse(content)

    return function_template 