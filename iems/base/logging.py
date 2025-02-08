from copy import deepcopy
from typing import Any
from structlog import configure, BytesLoggerFactory
from structlog.contextvars import merge_contextvars
from structlog.processors import (
    StackInfoRenderer,
    TimeStamper,
    add_log_level,
    dict_tracebacks,
    JSONRenderer,
)
from structlog.dev import ConsoleRenderer
from orjson import dumps
from iems.base.config import Config

__all__ = ["setup_logging"]


def setup_logging(*args, **kwargs):
    """
    Setup logging for the application.
    """

    def development_render(_, __, event_dict: dict[str, Any]) -> dict[str, Any]:
        """
        Renders log on console only if server is running in development mode
        Args:
            event_dict (dict[str,Any]): Contains context of the log

        Returns:
            dict[str,Any]:Context of the log for further processing by other proccessors
        """
        config = Config.get_config()
        if config.SERVER_ENVIRONMENT == "DEV":
            console_dict = deepcopy(event_dict)
            console = ConsoleRenderer()
            print(console.__call__(_, __, console_dict))
        return event_dict

    configure(
        processors=[
            merge_contextvars,
            add_log_level,
            StackInfoRenderer(),
            TimeStamper(fmt="iso"),
            development_render,
            dict_tracebacks,
            JSONRenderer(serializer=dumps),
        ],
        logger_factory=BytesLoggerFactory(open("./logs.json", "ab")),
        cache_logger_on_first_use=True,
    )
