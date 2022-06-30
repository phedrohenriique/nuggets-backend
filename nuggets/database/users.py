## handles all the queries and manipulate database information 

import logging
from sanic.log import logger
from connection import create_pool
from mappers import map_users


async def get_users_list_database():
    pool = await create_pool()
    connection = await pool.acquire()

    query_get = """
        SELECT id, name, email
        FROM users
    """

    try:
        result = await connection.fetch(query_get)  
        result = [map_users(result) for result in result]
        response = result
    except Exception as error :
        logger.exception("Failed to retrieve users list : ", error)
        return None

    finally:
        await pool.release(connection)
        return response

async def get_users(user_id):
    pool = await create_pool()
    connection = await pool.acquire()

    query_get_users = """
        SELECT *
        FROM users
        WHERE id = $1
    """

    response = []

    try:
        result = await connection.fetch(query_get_users, user_id)
        result = [map_users(result) for result in result]
        response = result[0]
    except Exception as error:
        logger.exception("Failed to get user : ", error)
        return None
    finally:
        await pool.release(connection)
        return response

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

    response = []

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

        response = {
            "message":"user created", 
            "id": id}
        await transaction.commit()

    except Exception as error:
        await transaction.rollback()
        logger.exception("Failed to register user : ", error)
        return None

    finally:
        await pool.release(connection)
        return response
    
async def post_users_login_database(data):
    pool = await create_pool()
    connection = await pool.acquire()

    query_login = """
        SELECT id, name, email, password
        FROM users
        WHERE email = $1
    """

    response = []

    try:
        result = await connection.fetch(query_login, data["email"])
        result = [map_users(result) for result in result]
        response = result[0]
       
    except Exception as error:
            logger.exception("Failed to login : ", error)
            return None         
    finally:
        await pool.release(connection)
        return response

async def patch_users_edit_database(user_id, data_update):
    pool = await create_pool()
    connection = await pool.acquire()
    transaction = connection.transaction()

    query_patch_user = """
        UPDATE users
        SET 
            name = $2,
            email = $3,
            password = $4
        WHERE id = $1
    """

    query_get_user = """
        SELECT id, name, email
        FROM users
        WHERE id = $1
    """

    response = []

    try:   

        await transaction.start()

        await connection.execute(
            query_patch_user, 
            user_id,
            data_update["name"],
            data_update["email"],
            data_update["password"]
            )

        result = await connection.fetch(
            query_get_user,
            user_id
        )

        result = [map_users(result) for result in result]
        response = {
            "message":"user updated",
            "user" : result[0]
        }

        await transaction.commit()
        
    except Exception as error:
        await transaction.rollback()
        logging.exception("Failed to update user : ", error)
        return None

    finally:
        await pool.release(connection)
        return response