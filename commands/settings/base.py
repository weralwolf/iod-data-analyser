from os import getenv
from logging import DEBUG
from os.path import join, dirname, realpath

from ionospheredata.configuration import isDir, ensureDir, assertConfig

BASE_DIR = join(realpath(dirname(__file__)), '..', '..')

ARTIFACTS_DIR = getenv('ARTIFACTS_DIR', join(BASE_DIR, 'artifacts'))
assertConfig(isDir(ARTIFACTS_DIR), 'One must set `ARTIFACTS_DIR`.')

CACHE_DIR = getenv('CACHE_DIR', join(ARTIFACTS_DIR, 'objects'))
TRACKS_DIR = join(ARTIFACTS_DIR, 'tracks')
LOGS_DIR = join(ARTIFACTS_DIR, 'logs')

ensureDir(CACHE_DIR)
ensureDir(TRACKS_DIR)
ensureDir(LOGS_DIR)

LOGGING_LEVEL = DEBUG
IS_SILENT = False
