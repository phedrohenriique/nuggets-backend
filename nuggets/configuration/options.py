from collections import defaultdict
from attr import frozen

from sanic import Sanic, response
from sanic.router import Route


def routes_options(routes):

    options = defaultdict(list)
    for route in routes.values():
        if "OPTIONS" not in route.methods :
            options = [route.uri].extend(route.methods)
    
    return { "uri": frozenset(methods) for uri, methods in dict(options).items()}

def options_wrapper(handler, methods):
    def wrapped_handler(request, *args, **kwargs):
        nonlocal methods ## keyword to determine that the variable is not local
        return handler(request, methods)
    
    return wrapped_handler

def options_handler(request, methods):
    response = response.empty()
    add_cors_headers(response, methods)

    return response

def setup_options(app: Sanic, _):
    app.router.reset()
    options = routes_options(app.router.routes_all)
    for uri, methods in options.items():
        app.add_route(
            options_wrapper(options_handler, methods),
            uri,
            methods=["OPTIONS"]
        )
    app.router.finalize()