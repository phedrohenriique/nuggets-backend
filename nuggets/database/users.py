## handles all the queries and manipulate database information 

from sanic.log import logger
from connection import create_pool
from configuration import (
    SECRET_KEY, 
    authorized
    )
from mappers import map_users


async def users_list_database():
    pool = await create_pool()
    connection = await pool.acquire()

    query = """
        SELECT id, name, email
        FROM users
    """

    try:
        result = await connection.fetch(query)  
        result = [map_users(result) for result in result]
    except Exception as error :
        logger.exception("Failed to retrieve users list", error)
        return None
    finally:
        await pool.release(connection)
        return result

async def post_user():
    pass