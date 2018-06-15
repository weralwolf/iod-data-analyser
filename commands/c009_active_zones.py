from matplotlib import use as setRenderingBackend  # isort:skip noqa:E402
setRenderingBackend('Agg')  # isort:skip

from os import makedirs  # noqa: E402
from os.path import join, basename  # noqa: E402
from datetime import datetime  # noqa: E402

from numpy import max, min, ceil, copy, array, zeros, absolute  # noqa: E402
from numpy.fft import rfft, irfft  # noqa: E402
from matplotlib import pyplot as plt  # noqa: E402
from scipy.signal import hilbert, argrelmax, argrelmin  # noqa: E402

from ionospheredata.utils import local_preload  # noqa: E402
from ionospheredata.parser import FileParser, SampledNACSRow  # noqa: E402
from ionospheredata.settings import ARTIFACTS_DIR  # noqa: E402

from .logger import logger  # noqa: E402
from .c007_moving_average import omit_zeros, remove_trend, segments_list, smooth_signal  # noqa: E402

RESULTS_DIR = join(ARTIFACTS_DIR, 'thesis_results')
makedirs(RESULTS_DIR, exist_ok=True)

"""
Task:
Here we're working only with oxygen component of NACS `o_dens`.

1. Select variation:
    1.1. Identify trend by moving average:
    1.2. De-trend input signal;
    1.3. Perform ideal filtration;
    1.4. Restore signal from spectra;
2. Identify active and sporadic zones:
    2.1. Build enveloping lines around squares of amplitudes;
    2.2. Identify bounds of packages by minimums of enveloping line;
    2.3. Identify location and length active packages as amplitude jumps ~0.1..0.3;
    2.4. Identify location and length sporadic packages as amplitude jumps ~0.1;
    2.5. Identify zones by longitudes;

Later read: http://www.di.fc.ul.pt/~jpn/r/fourier/fourier.html
"""


ZEROFILL_LENGTH = 2**16
SATELLITE_VELOCITY = 7.8
GW_MIN_WAVELENGTH = 100
GW_MAX_WAVELENGTH = 2500
MINIMUM_PERTURBATION_LENGTH = int(round(300. / SATELLITE_VELOCITY))


def zerofilled_bounds(original_length):
    start = (ZEROFILL_LENGTH - original_length) // 2
    return start, start + original_length


def zerofilled_signal(original):
    zerofilled = zeros(ZEROFILL_LENGTH)
    original_length = len(original)

    bs, be = zerofilled_bounds(original_length)

    zerofilled[bs:be] = original
    return zerofilled


def zerofilled_ut(ut, sampling):
    original_length = len(ut)
    bs, be = zerofilled_bounds(original_length)
    new_ut = array(list(range(0, ZEROFILL_LENGTH, sampling))) + min(ut)
    new_ut -= new_ut[bs]
    new_ut[bs:be] = ut
    return new_ut


def original_signal(signal, original_length):
    bs, be = zerofilled_bounds(original_length)
    return signal[bs:be]


def data_title(name, ut):
    return '{} {} - {}'.format(
        name,
        datetime.fromtimestamp(ut[0]).strftime('%Y.%j %H:%M:%S'),
        datetime.fromtimestamp(ut[-1]).strftime('%Y.%j %H:%M:%S')
    )


def lat_ticks(lat, ticks):
    return [lat[int(tick * (len(lat) - 1))] for tick in ticks]


def analyze_segment(sampling, segment_file):
    segment_data = local_preload(segment_file, FileParser, SampledNACSRow, segment_file)
    # ut = (segment_data.get('ut', transposed=True)[0] - 347155200) / 3600 - 5472
    ut = segment_data.get('ut', transposed=True)[0]
    lat = segment_data.get('lat', transposed=True)[0]
    o_dens = omit_zeros(segment_data.get('o_dens', transposed=True)[0])
    signal, trend = remove_trend(sampling, o_dens)

    original_length = len(o_dens)
    RO = lambda x: original_signal(x, original_length)  # noqa: E731

    signal = zerofilled_signal(signal)
    ut = zerofilled_ut(ut, sampling)

    parameter_name = 'Oxygen density'

    fig_name_filtering = join(RESULTS_DIR, basename(segment_file)[:-3] + 'filtering.png')
    fig_name_hilbert = join(RESULTS_DIR, basename(segment_file)[:-3] + 'hilbert.png')

    fig_filtering = plt.figure()
    ax_ut = fig_filtering.add_subplot(311)
    ax_lat = ax_ut.twiny()
    ax_lat.set_xticks(ax_ut.get_xticks())
    ax_lat.set_xticklabels(lat_ticks(lat, ax_ut.get_xticks()))
    ax_ut.plot(RO(ut), o_dens)
    ax_ut.plot(RO(ut), trend)
    ax_ut.legend([
        parameter_name,
        'Moving average',
    ])
    ax_ut.set(
        xlabel='Universal time, (s)',
        ylabel='Density, 1/cm^3',
    )
    ax_lat.set(
        xlabel='Latitude, (deg)'
    )

    # Signal information
    ax_ut = fig_filtering.add_subplot(323)
    ax_lat = ax_ut.twiny()
    ax_lat.set_xticks(ax_ut.get_xticks())
    ax_lat.set_xticklabels(lat_ticks(lat, ax_ut.get_xticks()))
    ax_ut.plot(RO(ut), RO(signal))
    ax_ut = fig_filtering.add_subplot(324)
    spectra = rfft(signal)
    frequencies = array(range(len(spectra)))  # rfftfreq(len(signal), 1.)
    ax_ut.plot(frequencies, absolute(spectra))

    min_threshold_index = int(round(ZEROFILL_LENGTH * SATELLITE_VELOCITY / GW_MIN_WAVELENGTH))
    max_threshold_index = int(round(ZEROFILL_LENGTH * SATELLITE_VELOCITY / GW_MAX_WAVELENGTH))
    # min_threshold_freq = 2 * pi * SATELLITE_VELOCITY / GW_MIN_WAVELENGTH
    # max_threshold_freq = 2 * pi * SATELLITE_VELOCITY / GW_MAX_WAVELENGTH

    new_spectra = copy(spectra)
    new_spectra[:max_threshold_index] = 0
    new_spectra[min_threshold_index:] = 0

    new_signal = irfft(new_spectra)

    # Signal information after filtering. Use signal 100..2500 km
    ax_ut = fig_filtering.add_subplot(325)
    ax_lat = ax_ut.twiny()
    ax_lat.set_xticks(ax_ut.get_xticks())
    ax_lat.set_xticklabels(lat_ticks(lat, ax_ut.get_xticks()))
    ax_ut.plot(RO(ut), RO(new_signal))

    ax_ut = fig_filtering.add_subplot(326)
    ax_ut.plot(frequencies, absolute(spectra), '-')
    ax_ut.plot(frequencies, absolute(new_spectra))

    fig_filtering.savefig(fig_name_filtering, dpi=300, papertype='a0', orientation='landscape')
    plt.close(fig_filtering)

    # Hilbert analysis
    fig_hilbert = plt.figure()
    ax_ut = fig_hilbert.add_subplot(111)
    ax_lat = ax_ut.twiny()
    ax_lat.set_xticks(ax_ut.get_xticks())
    ax_lat.set_xticklabels(lat_ticks(lat, ax_ut.get_xticks()))

    # 13s ~= 100km / 7.8km/s
    smoother = lambda x: smooth_signal(sampling, x, ceil(GW_MIN_WAVELENGTH / SATELLITE_VELOCITY))  # noqa: E731

    energy_signal = absolute(new_signal)
    smoothed_signal = energy_signal
    # smoothed_signal = smoother(energy_signal)

    analytic_signal_1 = hilbert(smoothed_signal)
    amplitude_envelope_1 = absolute(analytic_signal_1)

    analytic_signal_2 = hilbert(amplitude_envelope_1)
    amplitude_envelope_2 = absolute(analytic_signal_2)

    ax_ut.plot(RO(ut), RO(new_signal))
    # ax_ut.plot(RO(ut), RO(energy_signal))
    # ax_ut.plot(RO(ut), RO(smoothed_signal))
    # ax_ut.plot(RO(ut), amplitude_envelope_1)
    # ax_ut.plot(RO(ut), RO(amplitude_envelope_2))
    enveloping_line = RO(smoother(amplitude_envelope_2))
    ax_ut.plot(RO(ut), enveloping_line, '-')
    signal_line = RO(new_signal)

    for n, package in enumerate(select_packages(enveloping_line, 3)):
        # logger.error('{} - ratio: {} - diff: {}'.format(n, package['ratio'], package['diff']))
        ax_ut.plot(RO(ut)[package['start']:package['end']], signal_line[package['start']:package['end']])
        ax_ut.plot(RO(ut)[package['max_point']], enveloping_line[package['max_point']], 'x', color='blue')

    fig_hilbert.savefig(fig_name_hilbert, dpi=300, papertype='a0', orientation='landscape')
    plt.close(fig_hilbert)


def select_packages(signal, threshold):
    max_pre_ticks = array(*argrelmax(signal))
    min_pre_ticks = array(*argrelmin(signal))

    for max_point in max_pre_ticks:
        ps, pe = None, None

        # extend to the right
        for current_min in min_pre_ticks[min_pre_ticks > max_point]:
            if signal[current_min] > signal[max_point]:
                pe = None
                break

            pe = current_min
            if signal[max_point] / signal[current_min] >= threshold:
                break
        else:
            pe = len(signal) - 1

        # expand to the left
        for current_min in array(list(reversed(min_pre_ticks[min_pre_ticks < max_point]))):
            if signal[current_min] > signal[max_point]:
                ps = None
                break

            ps = current_min
            if signal[max_point] / signal[current_min] >= threshold:
                break
        else:
            ps = 0

        if ps is None or pe is None:
            continue

        pmin = min(signal[ps:pe])
        pmax = max(signal[ps:pe])

        if pmax / pmin <= threshold:
            continue

        yield dict(
            start=ps,
            end=pe,
            diff=pmax - pmin,
            ratio=pmax / pmin,
            max_point=max_point
        )


def main():
    sampling = 1
    segments = segments_list(sampling)[:1]
    segments_num = len(segments)
    for n, segment_file in enumerate(segments):
        logger.info('{} / {} - {}'.format(n + 1, segments_num, segment_file))
        analyze_segment(sampling, segment_file)


if __name__ == '__main__':
    main()
