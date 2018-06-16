from os import getenv
from logging import DEBUG
from os.path import join, dirname, realpath

from numpy import round

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

# DE 2 satellite velocity
SATELLITE_VELOCITY = 7.8  # km/s

# Atmospheric gravity waves estimated parameters
GW_MIN_WAVELENGTH = 200  # km
GW_MAX_WAVELENGTH = 2500  # km

# Analysis. Minimum length since we count signal spike of activity to be a perturbation
MINIMUM_PERTURBATION_LENGTH = 300.  # km
MINIMUM_PERTURBATION_TIME = int(round(MINIMUM_PERTURBATION_LENGTH / SATELLITE_VELOCITY))  # 1 sec ticks

# Analysis. Signal zero-extension, always must be power of 2. It extends FFT resolution
# and help to keep signals on the same scale.
ZEROFILL_LENGTH = 2**16  # signal data points
