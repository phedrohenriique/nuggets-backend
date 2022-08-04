## handlers all the function logic to be passe through the routes

from database import (
    get_users_database,
    get_users_list_database,
    post_users_database,
    post_users_login_database,
    patch_users_edit_database
    )
from configuration import SECRET_KEY
import hashlib as hs
import jwt

async def get_users_list_controller():
    users_list = await get_users_list_database()
    result = users_list

    return result

async def post_users_controller(data):
    if not (data.get("email") or data.get("password")):
        return None

    if not data.get("name"):
        data["name"] = ''
    
    ## password must be transformed into string, and .encode() method used so
    ## it transforms it into bytes so it can be used in hash and hexed

    data["password"] = str(data["password"]).encode()
    data["password"] = hs.sha256(data["password"]).hexdigest()

    result = await post_users_database(data)
    return result

async def post_users_login_controller(data):
    if not (data.get("email") or data.get("password")):
        return None
    
    data["password"] = str(data["password"]).encode()
    data["password"] = hs.sha256(data["password"]).hexdigest()
    
    user = await post_users_login_database(data)
    if data["password"] != user.get("password"):
        return None
    
    key = SECRET_KEY
    user_data = {
        "user": {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email")
        }
    }
    result = {
        "message": "user logged in",
        "token": jwt.encode(user_data, key, "HS256")
        }

    return result

async def patch_users_edit_controller(user_id, token, data):
    user = await get_users_database(user_id)

    data_user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    data_user = data_user["user"]
    data_user["password"] = user["password"]

    data_update = data
    if data_update.get("password"):
        data_update["password"] = str(data_update["password"]).encode()
        data_update["password"] = hs.sha256(data_update["password"]).hexdigest() 

    data_update["name"] = data_update["name"] if data_update.get("name") else data_user["name"]
    data_update["password"] = data_update["password"] if data_update.get("password") else data_user["password"]
    data_update["email"] = data_update["email"] if data_update.get("email") else data_user["email"]

    result = await patch_users_edit_database(user_id, data_update)
    
    return result