from numpy import zeros, concatenate
from numpy.fft import fft, ifft

from ionospheredata.consts import NFFT, GW_WINDOW_LEN

from .moving_average import moving_average


def gravitation_wave(concentration):
    """Computes a gravity wave by concentration function.
    @param concentration: is a concentration function over the time along satellite's trajectory. shape is (N, );
    @return (trend, wave, wave_fft, grav_wave)
        trend - global change of cnocentration. Obtained by smoothing;
        wave - is a concentration variation. Difference of concentration and trend;
        wave_fft - Fast Fourie Tranformation of wave;
        grav_wave - gravitational wave.
    """
    data_len = len(concentration)
    zero_fill = zeros((NFFT - data_len, ))
    extended_concentration = concatenate((concentration, zero_fill))
    # extended_concentration = concentration

    # trend by moving average
    trend = concatenate((moving_average(concentration, GW_WINDOW_LEN)[:data_len], zero_fill))  # calculate trend for data set
    # trend = smooth(concentration, GW_WINDOW_LEN)[:l]  # calculate trend for data set
    wave = extended_concentration - trend

    # fft by wave, what without trend
    wave_fft = fft(wave, NFFT)

    # GW creation just for DE 2 NACS 365T042320
    a = round(NFFT * 7.8 / 2500)  # in spectr with L = 2500 km
    b = round(NFFT * 7.8 / 100)  # in spectr with L = 250 km

    ffts_area = zeros((NFFT, ))
    ffts_area = concatenate((
        zeros((a, )),
        wave_fft[a:b],
        zeros((NFFT - 2 * b, )),
        wave_fft[NFFT - b:NFFT - a],
        zeros((a, ))
    ), axis=0)
    wave_ifft = ifft(ffts_area)
    grav_wave = wave_ifft / trend  # norm wave by height

    return trend, wave, wave_fft, grav_wave
