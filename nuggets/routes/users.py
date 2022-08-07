from controllers import (
    get_users_list_controller,
    post_users_controller,
    post_users_login_controller,
    patch_users_edit_controller,
    user_token_info_controller
    )
from configuration import (
    invalid_fields,
    database_error,
    not_authorized,
    success_response,
    error_response
    )
import sanic as sn
from configuration import authorized
from sanic import exceptions

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
        ##raise exceptions.ServerError("server error")
        return error_response(database_error)

    return success_response(result)

@users.post('/login')
async def users_login(request):
    data = request.json
    if not data:
        return error_response(invalid_fields)

    result = await post_users_login_controller(data)
    if not result:
        return error_response(not_authorized)
    
    return success_response(result)


@users.patch("/login/<user_id:uuid>/edit")
@authorized
async def user_update(request, user_id):
## can get token information without needing another query with request.token object from the route
    token = request.token
    data = request.json

    if not (token or data):
        return error_response(invalid_fields)

    response = await patch_users_edit_controller(user_id, token, data)
    if not response:
        return error_response(database_error)

    return success_response(response)
        
@users.get("/login/user")
@authorized
async def user_login(request):

    token = request.token
    response = await user_token_info_controller(token)

    if not response:
        return error_response(database_error)
    
    return success_response(response)
