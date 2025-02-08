from typing import Any, ClassVar
from structlog import get_logger
from sanic.handlers import ErrorHandler as BaseErrorHandler
from iems.base.models import UnkownExceptionModel
from iems.base.response import JSONResponse


class VeroperaException(BaseException):
    slug: ClassVar[str]
    description: ClassVar[str]
    context: dict[str, Any] = dict()


class ErrorHandler(BaseErrorHandler):
    def default(self, request, exception):
        if not issubclass(exception.__class__, VeroperaException):
            get_logger().error(
                event="unkonwn_exception",
                context={
                    "name": exception.__class__.__name__,
                    "msg": str(exception),
                    "context": exception.__dict__,
                },
            )
            return JSONResponse(UnkownExceptionModel().model_dump_json(), 500)
