import sanic as sn
import routes as rt
import configuration as config

## instantiated Sanic Server
## can start server with sanic repensa.app or python repensa.py (with app.run method)

app = sn.Sanic('nuggets')
app.blueprint(rt.routes)

app.config.CORS_ORIGINS = "*"  ## need to be setted to send response CORS allowed headers
app.config.RESPONSE_TIMEOUT = 1
app.config.REQUEST_TIMEOUT = 1

## app object will be running the routes = sn.Blueprint.group() where all the routes will be stated

app.run(host='0.0.0.0', port=config.PORT, debug=True, )