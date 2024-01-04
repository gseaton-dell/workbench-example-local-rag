"""Document Retrieval Service.

Handle document ingestion and retrieval from a VectorDB.
"""

import logging
import os
import sys
import typing

if typing.TYPE_CHECKING:
    from chatui.api import APIServer


_LOG_FMT = f"[{os.getpid()}] %(asctime)15s [%(levelname)7s] - %(name)s - %(message)s"
_LOG_DATE_FMT = "%b %d %H:%M:%S"
_LOGGER = logging.getLogger(__name__)


def bootstrap_logging(verbosity: int = 0) -> None:
    """Configure Python's logger according to the given verbosity level.

    :param verbosity: The desired verbosity level. Must be one of 0, 1, or 2.
    :type verbosity: typing.Literal[0, 1, 2]
    """
    # determine log level
    verbosity = min(2, max(0, verbosity))  # limit verbosity to 0-2
    log_level = [logging.WARN, logging.INFO, logging.DEBUG][verbosity]

    # configure python's logger
    logging.basicConfig(filename='chatui.log', filemode='w',format=_LOG_FMT, datefmt=_LOG_DATE_FMT, level=log_level)
    # update existing loggers
    _LOGGER.setLevel(logging.DEBUG)
    for logger in [
        __name__,
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        for handler in logging.getLogger(logger).handlers:
            handler.setFormatter(logging.Formatter(fmt=_LOG_FMT, datefmt=_LOG_DATE_FMT))
