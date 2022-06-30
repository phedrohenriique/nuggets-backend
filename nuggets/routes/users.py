from controllers import (
    get_users_list_controller,
    post_users_controller,
    post_users_login_controller,
    patch_users_edit_controller
    )
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
from configuration import authorized

users = sn.Blueprint('users', url_prefix='/users')

@users.get('/')
async def get_users_list(request):
    users_list = await get_users_list_controller()

    if not users_list:
        return error_response(database_error)

    return success_response(users_list)

@users.post('/')
async def post_users(request):
    data = request.json
    if not data:
        return error_response(invalid_fields)

    result = await post_users_controller(data)
    if not result:
        return error_response(database_error)

    return success_response(result)

@users.post('/login')
async def users_login(request):
    data = request.json
    if not data:
        return error_response(invalid_fields)

    result = await post_users_login_controller(data)
    if not result:
        error_response(not_authorized)
    
    return success_response(result)


@users.patch("login/<user_id:uuid>/edit")
@authorized
async def user_update(request, user_id):
## can get token information without needing another query with request.token object from the route
    token = request.token
    data = request.json
    print(data)
    if not (token or data):
        return error_response(invalid_fields)

    response = await patch_users_edit_controller(user_id, token, data)

    return success_response(response)
        
