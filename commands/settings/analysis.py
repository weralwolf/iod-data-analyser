from numpy import round

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
