## handles all the queries and manipulate database information 

from psycopg2 import connect
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
        logger.exception("Failed to retrieve users list : ", error)
        return None

    finally:
        await pool.release(connection)
        return result

async def post_users_database(data):
    
    pool = await create_pool()
    connection = await pool.acquire()
    transaction = connection.transaction()

## transaction block starts, with create a situation in all the queries are
## executed or not, returning to a previous point of db

    query_post = """
        INSERT INTO users (name, email, password)
        VALUES ($1, $2, $3)
    """
    query_get = """
        SELECT id
        FROM users
        WHERE email = $1
    """
    try:
        await transaction.start()
        result = await connection.execute(
            query_post, 
            data["name"],
            data["email"],
            data["password"]
        )

        if result:
            id = await connection.fetch(query_get, data["email"])
            id = str(id[0].get("id"))

        await transaction.commit()

    except Exception as error:
        await transaction.rollback()
        logger.exception("Failed to register user : ", error)
        return None

    finally:
        await pool.release(connection)
        return id
    