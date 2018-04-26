from sys import stderr, stdout
from logging import INFO, DEBUG, ERROR, Formatter, StreamHandler, getLogger
from os.path import join
from logging.handlers import TimedRotatingFileHandler

from ionospheredata.settings import LOGS_DIR, IS_SILENT, LOGGING_LEVEL

logger = getLogger('iod')
logger.setLevel(LOGGING_LEVEL or DEBUG)

file_handler = TimedRotatingFileHandler(join(LOGS_DIR, 'iod.log'), when='H', interval=1, utc=True)
file_handler.setLevel(LOGGING_LEVEL or INFO)
filelog_formatter = Formatter('%(asctime)s::%(name)s:/%(filename)s # %(funcName)s ~ %(levelname)s# %(message)s')
file_handler.setFormatter(filelog_formatter)
logger.addHandler(file_handler)

if not IS_SILENT:
    stdout_handler = StreamHandler(stream=stdout)
    stdout_handler.setLevel(LOGGING_LEVEL or INFO)
    stdout_formatter = Formatter('%(name)s::%(filename)s/%(funcName)s # %(message)s')
    stdout_handler.setFormatter(stdout_formatter)
    logger.addHandler(stdout_handler)

stderr_handler = StreamHandler(stream=stderr)
stderr_handler.setLevel(ERROR)
error_formatter = Formatter('%(asctime)s::%(name)s:/%(filename)s # %(funcName)s ~ %(levelname)s# %(message)s')
stderr_handler.setFormatter(error_formatter)
logger.addHandler(stderr_handler)
