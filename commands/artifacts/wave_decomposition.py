from typing import Tuple
from commands.utils.logger import logger  # noqa: F401
from commands.settings.analysis import ZEROFILL_LENGTH, GW_MAX_WAVELENGTH, GW_MIN_WAVELENGTH, SATELLITE_VELOCITY
from commands.utils.local_cache import LocalCache
from commands.parsers.file_parser import FileParserWindow
from commands.artifacts.moving_average import moving_average

from numpy import copy, array, zeros
from numpy.fft import rfft, irfft


def zerofilled_bounds(original_length: int) -> Tuple[int, int]:
    start = (ZEROFILL_LENGTH - original_length) // 2
    return start, start + original_length


def zerofilled_signal(original: array) -> array:
    zerofilled = zeros((original.shape[0], ZEROFILL_LENGTH))
    original_length = original.shape[1]

    bs, be = zerofilled_bounds(original_length)

    zerofilled[:, bs:be] = original
    return zerofilled


def original_signal(signal: array, original_length: int) -> array:
    bs, be = zerofilled_bounds(original_length)
    return signal[:, bs:be]


def ideal_signal_filter(wave: array, sampling: int) -> Tuple[array, array, array]:
    original_length = wave.shape[1]
    signal = zerofilled_signal(wave)
    spectra = rfft(signal)

    min_threshold_index = int(round(ZEROFILL_LENGTH * sampling * SATELLITE_VELOCITY / GW_MIN_WAVELENGTH))
    max_threshold_index = int(round(ZEROFILL_LENGTH * sampling * SATELLITE_VELOCITY / GW_MAX_WAVELENGTH))

    trimmed_spectra = copy(spectra)
    trimmed_spectra[:, :max_threshold_index] = 0
    trimmed_spectra[:, min_threshold_index:] = 0
    trimmed_signal = original_signal(irfft(trimmed_spectra), original_length)

    lf_area_spectra = copy(spectra)
    lf_area_spectra[:, max_threshold_index:] = 0
    lf_signal = original_signal(irfft(lf_area_spectra), original_length)

    hf_area_spectra = copy(spectra)
    hf_area_spectra[:, :min_threshold_index] = 0
    hf_signal = original_signal(irfft(hf_area_spectra), original_length)

    return trimmed_signal, lf_signal, hf_signal


@LocalCache()
def wave_decomposition(data_chunk: FileParserWindow, *params_list: str, sampling: int = 1) -> Tuple[array, array, array]:
    value = data_chunk.get(*params_list, transposed=True)
    rough_trend = moving_average(data_chunk, *params_list, window_size=701)
    wave = value - rough_trend
    gw, lf_trend, noise = ideal_signal_filter(wave, sampling)
    return gw, rough_trend + lf_trend, noise
