import logging
from enum import Enum
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.DEBUG)
ENV = config("ENV", default="local")
TEMP_FOLDER = config("TEMP_FOLDER", default=None)
EXCLUDE_FOLDERS = config("EXCLUDE_FOLDERS", default=None, cast=CommaSeparatedStrings)
MEDIA_EXTENSIONS = config("MEDIA_EXTENSIONS", default=None, cast=CommaSeparatedStrings)
APP_MEDIA_SCAN_DIRS = config(
    "APP_MEDIA_SCAN_DIRS", default=None, cast=CommaSeparatedStrings
)


class BaseEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


LOG_FORMAT = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(BaseEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging():
    log_level = str(LOG_LEVEL).upper()  # cast to string
    log_levels = list(LogLevels)

    if log_level not in log_levels:
        # we use error as the default log level
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT)
        return

    logging.basicConfig(level=log_level)


configure_logging()
