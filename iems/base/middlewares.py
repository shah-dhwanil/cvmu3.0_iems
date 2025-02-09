from structlog.contextvars import clear_contextvars, bind_contextvars
from sanic import Request, Sanic
from structlog import get_logger
from sanic.response.types import HTTPResponse
from iems.auth.middlewares import auth_middleware

__all__ = ["register_middlewares"]


def add_context(request: Request):
    """
    Binds logging contet for each request.
    """
    if request.ctx.user is None:
        user_id = None
    else:
        user_id = request.ctx.user.user_id
    bind_contextvars(request_id=str(request.id), user_id=user_id)


def destroy_context(*_):
    """
    Clears logging context for each request after the responses are generated.
    """
    clear_contextvars()


def log_request(request: Request):
    """
    Logs each request
    """
    logger = get_logger()

    logger.info(
        event="request_received",
        route=request.endpoint,
        method=request.method,
        user_ip=request.client_ip,
        payload=len(request.body),
    )


def log_response(request: Request, response: HTTPResponse):
    """
    Logs each response coressponding to a request
    """
    logger = get_logger()
    logger.info(
        event="response_sent",
        route=request.endpoint,
        method=request.method,
        user_ip=request.client_ip,
        payload=len(response.body),
    )


def register_middlewares(app: Sanic):
    """
    Register all the middleware in required order to the Sanic Application
    """
    app.register_middleware(auth_middleware, "request")
    app.register_middleware(add_context, "request")
    app.register_middleware(log_request, "request")
    app.register_middleware(destroy_context, "response")
    app.register_middleware(log_response, "response")
