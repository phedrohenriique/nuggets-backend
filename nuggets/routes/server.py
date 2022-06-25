import sanic as sn
import configuration as config
import jwt

from connection import create_pool
from configuration import authorized, SECRET_KEY

server = sn.Blueprint('server',url_prefix='/server')

## routes being setted with sn.Blueprint() method and exported
## all routes can be acessed within the main file

@server.get('/')
async def server_start(request):
    print('server startd')
    return sn.json({ "message": f"server is running on PORT : {config.PORT}"})

@server.get('/env')
async def server_variables(request):
    print(config.PORT)
    return sn.json({"message":f"PORT : {config.PORT}"})

@server.get('/user')
async def server_user(request):
    query = """
        SELECT name, email 
        FROM users 
        WHERE name = 'pedro'
    """
    pool = await  create_pool()
    connection = await  pool.acquire()

    ## setting the .acquire() method allows for connecting and use db
    ## connection.transaction() necessar for more than one queries

    result = await connection.fetch(query)

    ## print(results, *results) the fetch result returns a list, with a record type variable
    ## in order to use and parse easily the parameters the result must have its arguments
    ## all used out of list, thats why use *results wich is the same as result[0]
    ## specificall for one list returned value query, if there were more results,
    ## another list should be done in an array

    response = [dict(result) for result in result]

    connection.close()
    return  sn.json(response, 200)

@server.get('/allusers')
async def server_users(request):
    query="""
        SELECT name, email 
        FROM users
    """
    pool = await create_pool()
    connection = await pool.acquire()
    result = await connection.fetch(query)
    
    result = [dict(result) for result in result]
    response = result
    

    return sn.json(response, 200)

@server.get('/authorized')
@authorized
async def get_authorized_info(request):
    token_data = jwt.decode(request.token, SECRET_KEY, algorithms=["HS256"])
    
    return sn.json(token_data)

## middleware is executed in order if it is request type

# @server.middleware("request")
# async def passing_middleware(request):
#     print("passing middleware")

#     return sn.json({"message":"middleware_route"})

@server.get('/example/<route_params:str>')
async def route_example_route_params(request, route_params):

    return sn.json({"route_params": route_params})

@server.get('/example')
async def route_example_route_args(request):

    route_args = request.args.get("args", None)
    return sn.json({"args": route_args})