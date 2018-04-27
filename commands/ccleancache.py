from os import remove, listdir
from fnmatch import fnmatch
from os.path import join

from ionospheredata.settings import CACHE_DIR

from .logger import logger


def main():
    removed = 0
    for fname in listdir(CACHE_DIR):
        if fnmatch(fname, '*.pydata'):
            logger.debug('Removing {}'.format(fname))
            remove(join(CACHE_DIR, fname))
            removed += 1
    logger.info('Removed {} files'.format(removed))
