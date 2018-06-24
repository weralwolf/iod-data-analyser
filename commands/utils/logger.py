from sys import stdout
from logging import INFO, DEBUG, Formatter, StreamHandler, getLogger
from os.path import join
from logging.handlers import TimedRotatingFileHandler
from commands.settings.base import LOGS_DIR, LOGGING_LEVEL

from .chalk import green, yellow, dim_grey, dim_light_grey

logger = getLogger('iod')
logger.setLevel(LOGGING_LEVEL or DEBUG)


file_handler = TimedRotatingFileHandler(join(LOGS_DIR, 'iod.log'), when='H', interval=1, utc=True)
file_handler.setLevel(LOGGING_LEVEL or INFO)
filelog_formatter = Formatter('%(asctime)s::%(name)s:/%(filename)s # %(funcName)s ~ %(levelname)s# %(message)s')
file_handler.setFormatter(filelog_formatter)
logger.addHandler(file_handler)

stdout_handler = StreamHandler(stream=stdout)
stdout_handler.setLevel(LOGGING_LEVEL or INFO)
stdout_formatter = Formatter(
    dim_grey('%(asctime)s::%(name)s:/') +
    dim_light_grey('%(filename)s # %(funcName)s ~ ') +
    yellow('%(levelname)s') +
    dim_grey(' # ') +
    green('%(message)s')
)
stdout_handler.setFormatter(stdout_formatter)
logger.addHandler(stdout_handler)
