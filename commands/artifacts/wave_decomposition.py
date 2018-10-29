from typing import Tuple
from commands.settings.analysis import ZEROFILL_LENGTH, GW_MAX_WAVELENGTH, GW_MIN_WAVELENGTH, SATELLITE_VELOCITY
from commands.utils.local_cache import LocalCache
from commands.utils.logger import logger
from commands.parsers.file_parser import FileParserWindow
from commands.artifacts.moving_average import moving_average

from numpy import copy, array, zeros, average
from numpy.fft import rfft, irfft
from logging import getLogger


def zerofilled_bounds(original_length: int) -> Tuple[int, int]:
    start = (ZEROFILL_LENGTH - original_length) // 2
    return start, start + original_length


def zerofilled_signal(original: array) -> array:
    zerofilled = zeros(ZEROFILL_LENGTH)
    original_length = len(original)

    bs, be = zerofilled_bounds(original_length)

    zerofilled[bs:be] = original
    return zerofilled


def original_signal(signal: array, original_length: int) -> array:
    bs, be = zerofilled_bounds(original_length)
    return signal[bs:be]


def ideal_signal_filter(wave: array, sampling: int) -> Tuple[array, array, array]:
    original_length = len(wave)
    signal = zerofilled_signal(wave)
    spectra = rfft(signal)

    min_threshold_index = int(round(ZEROFILL_LENGTH * sampling * SATELLITE_VELOCITY / GW_MIN_WAVELENGTH))
    max_threshold_index = int(round(ZEROFILL_LENGTH * sampling * SATELLITE_VELOCITY / GW_MAX_WAVELENGTH))

    new_spectra = copy(spectra)
    new_spectra[:max_threshold_index] = 0
    new_spectra[min_threshold_index:] = 0

    trend_spectra = copy(spectra)
    trend_spectra[max_threshold_index:] = 0

    noise_spectra = copy(spectra)
    noise_spectra[:min_threshold_index] = 0

    new_signal = original_signal(irfft(new_spectra), original_length)
    trend_filtered = original_signal(irfft(trend_spectra), original_length)
    noise = original_signal(irfft(noise_spectra), original_length)

    return new_signal, trend_filtered, noise


@LocalCache()
def wave_decomposition(data_chunk: FileParserWindow, *params_list: str, sampling: int=1) -> array:  # Tuple[array, array, array]:
    value = data_chunk.get(*params_list, transposed=True)
    moving_average_trend = moving_average(data_chunk, *params_list)
    waves = value - moving_average_trend
    return array([(wave, trend + moving_average_trend, noise) for wave, trend, noise in [ideal_signal_filter(wave, sampling) for wave in waves]])
