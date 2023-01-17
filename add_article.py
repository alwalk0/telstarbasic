from articles import articles, database
import asyncio


TITLE = 'Functional Programming in Python: When and How to Use It'
URL = 'https://realpython.com/python-functional-programming/#how-well-does-python-support-functional-programming'



async def add_article():

    await database.connect()
    
    query = articles.insert().values(
    title=TITLE,
    url=URL)

    await database.execute(query)


asyncio.run(add_article()) 
