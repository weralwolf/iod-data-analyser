from os import getenv
from logging import DEBUG
from os.path import join, dirname, realpath

from .configuration import isDir, ensureDir, assertConfig

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

# class Settings:
#     BASE_DIR = join(realpath(dirname(__file__)), '..', '..')

#     DE2SOURCE_NACS_DIR = getenv('DE2SOURCE_NACS_DIR', None)
#     DE2SOURCE_WATS_DIR = getenv('DE2SOURCE_WATS_DIR', None)
#     ARTIFACTS_DIR = getenv('ARTIFACTS_DIR', None)

#     LOGGING_LEVEL = DEBUG
#     IS_SILENT = False

#     def __init__(self):
#         self.validate()
#         self.setup()

#     def validate(self):
#         assertConfig(isDir(self.DE2SOURCE_NACS_DIR), 'One must set `DE2SOURCE_NACS_DIR`.')
#         assertConfig(isDir(self.DE2SOURCE_WATS_DIR), 'One must set `DE2SOURCE_WATS_DIR`.')
#         assertConfig(isDir(self.ARTIFACTS_DIR), 'One must set `ARTIFACTS_DIR`.')

#     def setup(self):
#         self.CACHE_DIR = getenv('CACHE_DIR', join(self.ARTIFACTS_DIR, 'objects'))
#         self.DE2_NACS_DIR = getenv('NACS_DIR', join(self.ARTIFACTS_DIR, 'nacs'))
#         self.DE2_WATS_DIR = getenv('WATS_DIR', join(self.ARTIFACTS_DIR, 'wats'))
#         self.TRACKS_DIR = join(self.ARTIFACTS_DIR, 'tracks')
#         self.LOGS_DIR = join(self.ARTIFACTS_DIR, 'logs')
#         ensureDir(self.CACHE_DIR)
#         ensureDir(self.DE2_NACS_DIR)
#         ensureDir(self.DE2_WATS_DIR)
#         ensureDir(self.TRACKS_DIR)
#         ensureDir(self.LOGS_DIR)
