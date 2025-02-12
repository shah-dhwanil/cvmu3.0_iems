from sanic import Sanic
from sanic.response import text
from orjson import dumps, loads
from iems.base.listners import register_listners
from iems.base.exceptions import ErrorHandler
from iems.base.middlewares import register_middlewares
from iems.base.blueprints import register_blueprints

app = Sanic(
    "iems",
    dumps=dumps,
    loads=loads,
    error_handler=ErrorHandler(),
    configure_logging=False,
)
register_listners(app)
register_middlewares(app)
register_blueprints(app)
app.config.CORS_ORIGINS = "*"


@app.get("/")
async def hello_world(request, **kwargs):
    return text("Hello World")
