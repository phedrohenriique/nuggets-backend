## handlers all the function logic to be passe through the routes
import hashlib as hs
from database import (
    users_list_database,
    post_users_database
    )

async def users_list_controller():
    users_list = await users_list_database()
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