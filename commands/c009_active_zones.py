from matplotlib import use as setRenderingBackend  # isort:skip noqa:E402
setRenderingBackend('Agg')  # isort:skip

from os import makedirs  # noqa: E402
from os.path import join, basename  # noqa: E402
from datetime import datetime  # noqa: E402
from commands.parsers import FileParser, SampledNACSRow  # noqa: E402
from commands.utils.logger import logger  # noqa: E402

from numpy import abs, max, min, ceil, array, where, zeros, absolute  # noqa: E402
from matplotlib import pyplot as plt  # noqa: E402
from scipy.signal import hilbert, argrelmax, argrelmin  # noqa: E402

from ionospheredata.utils import local_preload  # noqa: E402
from ionospheredata.settings import ARTIFACTS_DIR, ZEROFILL_LENGTH, GW_MIN_WAVELENGTH, SATELLITE_VELOCITY  # noqa: E402

from .c007_moving_average import omit_zeros, remove_trend, segments_list, smooth_signal  # noqa: E402

RESULTS_DIR = join(ARTIFACTS_DIR, 'samplings', '001')
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


def discrete_ticks(lat, precision=5.0):
    ticks = []
    labels = []
    last_tick = None
    lat_l = len(lat)
    for idx, lat_v in enumerate(lat):
        tick_value = (lat_v // precision) * precision
        if tick_value != last_tick:
            last_tick = tick_value
            ticks.append(idx / lat_l)
            labels.append(tick_value)

    return ticks, labels


def hours_ticks(hours):
    hours_i = [int(hour * 50) / 50. for hour in hours]
    return list(sorted(list(set(hours_i))))


def ut_to_hours(uts):
    return array([ut / 3600000. for ut in uts])


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def analyze_segment(sampling, segment_file):
    segment_data = local_preload(segment_file, FileParser, SampledNACSRow, segment_file)
    ut = segment_data.get('ut', transposed=True)[0]
    lat = segment_data.get('lat', transposed=True)[0]
    lon = segment_data.get('lon', transposed=True)[0]
    o_dens = omit_zeros(segment_data.get('o_dens', transposed=True)[0])
    hours = ut_to_hours(ut)

    signal, trend, fft_trend, noise = remove_trend(sampling, o_dens)

    original_length = len(o_dens)
    RO = lambda x: original_signal(x, original_length)  # noqa: E731

    signal = zerofilled_signal(signal)
    # ut = zerofilled_ut(ut, sampling)

    fig_name_hilbert = join(RESULTS_DIR, basename(segment_file)[:-3] + 'hilbert.png')

    # Hilbert analysis
    fig_hilbert = plt.figure()
    ax_hours_hilbert = fig_hilbert.add_subplot(111)
    lat_t, lat_l = discrete_ticks(lat)
    lon_t, lon_l = discrete_ticks(lon, precision=.5)
    hours_m = hours_ticks(hours)

    ax_lon_trend = ax_hours_hilbert.twiny()
    ax_lon_trend.grid(True)
    ax_lon_trend.spines['top'].set_position(('axes', 1.08))
    make_patch_spines_invisible(ax_lon_trend)
    ax_lon_trend.spines['top'].set_visible(True)
    plt.setp(ax_lon_trend.xaxis.get_majorticklabels(), rotation=-90)
    ax_lon_trend.xaxis.set_tick_params(labelsize=4)
    ax_lon_trend.set_xticks(lon_t)
    ax_lon_trend.set_xticklabels(lon_l)

    ax_lat_trend = ax_hours_hilbert.twiny()
    ax_lat_trend.set_xticks(lat_t)
    ax_lat_trend.set_xticklabels(lat_l)
    plt.setp(ax_lat_trend.xaxis.get_majorticklabels(), rotation=-90)
    ax_lat_trend.xaxis.set_tick_params(labelsize=4)

    # 13s ~= 100km / 7.8km/s
    smoother = lambda x: smooth_signal(sampling, x, ceil(GW_MIN_WAVELENGTH / SATELLITE_VELOCITY))  # noqa: E731

    energy_signal = absolute(signal)
    smoothed_signal = energy_signal

    analytic_signal_1 = hilbert(smoothed_signal)
    amplitude_envelope_1 = absolute(analytic_signal_1)

    analytic_signal_2 = hilbert(amplitude_envelope_1)
    amplitude_envelope_2 = absolute(analytic_signal_2)

    ax_hours_hilbert.plot(hours, RO(signal))
    enveloping_line = RO(smoother(amplitude_envelope_2))
    ax_hours_hilbert.plot(hours, enveloping_line, '-')
    signal_line = RO(signal)

    packages_to_write = []

    trend_full = trend + fft_trend

    for n, package in enumerate(select_packages(enveloping_line, 3)):
        relative = abs(signal_line[package['start']:package['end']] / trend_full[package['start']:package['end']])
        max_value = max(relative)
        max_location = package['start'] + where(relative == max_value)[0][0]
        max_lat = lat[max_location]
        packages_to_write.append([
            basename(segment_file)[:7],
            ut[package['start']], lat[package['start']], lon[package['start']],
            ut[package['end']], lat[package['end']], lon[package['end']],
            max_value,
            max_lat,
        ])
        ax_hours_hilbert.plot(hours[package['start']:package['end']], signal_line[package['start']:package['end']])
        ax_hours_hilbert.plot(hours[package['max_point']], enveloping_line[package['max_point']], 'x', color='blue')

    maximums = {pack[-1] for pack in packages_to_write}

    for maximum in maximums:
        packs = [pack for pack in packages_to_write if pack[-1] == maximum]
        left_pack = sorted(packs, key=lambda p: p[1])[0]
        right_pack = sorted(packs, key=lambda p: p[4])[-1]
        logger.error('package::\t{};{};{};{};{};{};{};{:.4f};{}'.format(*left_pack[:4], *right_pack[4:]))

    ax_hours_hilbert.set_xticks(hours_m)
    plt.setp(ax_hours_hilbert.xaxis.get_majorticklabels(), rotation=-30)
    ax_hours_hilbert.xaxis.set_tick_params(labelsize=4)

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
    segments = segments_list(sampling)
    for n, segment_file in enumerate(segments):
        analyze_segment(sampling, segment_file)


if __name__ == '__main__':
    main()
