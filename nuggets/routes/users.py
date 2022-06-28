from database import get_users_list
from configuration import (
    invalid_fields,
    database_error,
    not_authorized,
    success_response,
    error_response
)
import sanic as sn
from connection import create_pool
from mappers import map_users
import hashlib as hs
from configuration import SECRET_KEY, authorized
import jwt

users = sn.Blueprint('users', url_prefix='/users')

@users.get('/')
async def get_users(request):
    users_list = await get_users_list()
    if not users_list:
        return error_response(database_error)
    return success_response(users_list)

@users.post('/')
async def post_users(request):
    pool = await create_pool()
    connection = await pool.acquire()

    name = request.json.get('name')
    email = request.json.get('email')
    password = str(request.json.get('password'))

    query = """
        INSERT INTO users (name, email, password)
        VALUES ($1, $2, $3)
    """
    try:

    ## password must be transformed into string, and .encode() method used so
    ## it transforms it into bytes so it can be used in hash and hexed

        password = password.encode()
        password = hs.sha256(password).hexdigest()
        await connection.execute(query, name, email, password)
        return sn.json({"message": "user registered"})
    except Exception as error:
        print(f"{error}")
        return sn.json({"message": f"{error}"})

@users.post('/login')
async def users_login(request):
    pool = await create_pool()
    connection = await pool.acquire()
    
    email = request.json.get('email')
    password = request.json.get('password')
    hash_password = hs.sha256(str(password).encode()).hexdigest()

    query_login = """
        SELECT id, name, email, password
        FROM users
        WHERE email = $1
    """
    try:
        result = await connection.fetch(query_login, email)
        result = [map_users(result) for result in result]
        db_password = result[0].get('password')
        if db_password != hash_password:
            return
        if db_password == hash_password:

            key = SECRET_KEY
            payload = {
                "message": "user logged in",
                "user": {
                    "id": result[0].get("id"),
                    "email": result[0].get("email"),
                    "name": result[0].get("name")
                }
            }
            token = jwt.encode(payload, key, "HS256")
            return sn.json({"token":token, "data": payload})
    except Exception as error:
        print(f"{error}")
        return sn.json({"message": f"{error}"}, 400)


@users.patch("login/<user_id:uuid>/edit")
@authorized
async def user_update(request, user_id):
    pool = await create_pool()
    connection = await pool.acquire()

    id = user_id
    name = request.json.get("name")
    email = request.json.get("email")
    password = str(request.json.get("password"))

    query = """
        UPDATE users
        SET 
            name = $2,
            email = $3,
            password = $4
        
        WHERE id = $1
        RETURNING id, name, email
    """
    try:
        password = password.encode()
        password = hs.sha256(password).hexdigest()

        result = await connection.fetch(query, id, name, email, password)
        result = [map_users(result) for result in result]
        return sn.json({"message": "user updated", "data": result[0]})
    except Exception as error:
         print(f'{error}')
         return sn.json({"message:" : f"{error}"}, 501)
        
