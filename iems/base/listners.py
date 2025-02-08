from sanic import Sanic
from uvloop import Loop
from iems.base.postgres import PGConnection
from iems.base.logging import setup_logging


async def initiate_pg_pool(_, loop: Loop):
    await PGConnection.initiate(loop)


async def close_pg_pool(_, __):
    await PGConnection.close()


def register_listners(app: Sanic):
    app.register_listener(setup_logging, "before_server_start")
    app.register_listener(initiate_pg_pool, "before_server_start")
    app.register_listener(close_pg_pool, "after_server_stop")
