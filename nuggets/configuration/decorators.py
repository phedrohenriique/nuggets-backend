from functools import wraps
from configuration import SECRET_KEY
import sanic as sn
import jwt

## standard function to get if the user is authorized
## token must be send as Authentication : Bearer Token in the header

def check_token(request):
    if not request.token:
        return False
    try:
        jwt.decode(request.token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.exceptions.InvalidTokenError:
        return False
        
## using decorators to create common handlers in applications

def authorized(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            ## checks the client authorization
            is_authorized = check_token(request)

            if is_authorized:
                ## user is authorized
                ## return the handler
                response = await f(request, *args, **kwargs)
                return response
            else :
                return sn.json({"status": "not_authorized"}, 403)
        return decorated_function
    return decorator(wrapped)