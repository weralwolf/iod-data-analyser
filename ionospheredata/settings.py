from os import getenv
from logging import DEBUG
from os.path import join, dirname, realpath

from .utils.configuration import isDir, ensureDir, assertConfig

BASE_DIR = join(realpath(dirname(__file__)), '..', '..')

DE2SOURCE_NACS_DIR = getenv('DE2SOURCE_NACS_DIR', None)
DE2SOURCE_WATS_DIR = getenv('DE2SOURCE_WATS_DIR', None)
ARTIFACTS_DIR = getenv('ARTIFACTS_DIR', None)

assertConfig(isDir(DE2SOURCE_NACS_DIR), 'One must set `DE2SOURCE_NACS_DIR`.')
assertConfig(isDir(DE2SOURCE_WATS_DIR), 'One must set `DE2SOURCE_WATS_DIR`.')
assertConfig(isDir(ARTIFACTS_DIR), 'One must set `ARTIFACTS_DIR`.')

CACHE_DIR = getenv('CACHE_DIR', join(ARTIFACTS_DIR, 'objects'))
DE2_NACS_DIR = getenv('NACS_DIR', join(ARTIFACTS_DIR, 'nacs'))
DE2_WATS_DIR = getenv('WATS_DIR', join(ARTIFACTS_DIR, 'wats'))
TRACKS_DIR = join(ARTIFACTS_DIR, 'tracks')
LOGS_DIR = join(ARTIFACTS_DIR, 'logs')

ensureDir(CACHE_DIR)
ensureDir(DE2_NACS_DIR)
ensureDir(DE2_WATS_DIR)
ensureDir(TRACKS_DIR)
ensureDir(LOGS_DIR)

LOGGING_LEVEL = DEBUG
IS_SILENT = False
