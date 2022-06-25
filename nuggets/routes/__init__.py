import sanic as sn
from .server import server
from .users import users

## if used the statement $import server will reference the server.py file while
## $from .server import server will import the variable inside the server.py file
## the __init__.py file is used to export all ./dir files, in an example, when
## acessing /routes the __init__.py loads and passes all variables and functions
## if the variables are being imported alone they can be used with their own name,
## example server from .server relating to file else the shall be used as module syntax,
## example as sanic as sn, sn.method() relating to directory

## file where to put all route Blueprint objects, for organization each route will have its
## own handler to be dealt and url

routes = sn.Blueprint.group(
    server,
    users,
    url_prefix='/')