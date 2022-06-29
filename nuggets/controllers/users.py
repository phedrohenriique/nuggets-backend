## handlers all the function logic to be passe through the routes

from database import users_list_database

async def users_list_controller():
    users_list = await users_list_database()

    return users_list