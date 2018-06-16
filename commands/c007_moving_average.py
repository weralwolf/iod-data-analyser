from matplotlib import use as setRenderingBackend  # isort:skip noqa:E402
setRenderingBackend('Agg')  # isort:skip

from os import listdir  # noqa: E402
from time import mktime  # noqa: E402
from fnmatch import fnmatch  # noqa: E402
from os.path import join, basename  # noqa: E402
from datetime import date, datetime  # noqa: E402

from numpy import nan, copy, array, isnan, zeros, absolute  # noqa: E402
from numpy.fft import rfft, irfft  # noqa: E402
from matplotlib import pyplot as plt  # noqa: E402

from ionospheredata.utils import local_preload  # noqa: E402
from ionospheredata.method import moving_average  # noqa: E402
from ionospheredata.parser import FileParser, SampledNACSRow  # noqa: E402
from ionospheredata.settings import (  # noqa: E402
    ARTIFACTS_DIR, ZEROFILL_LENGTH, GW_MAX_WAVELENGTH, GW_MIN_WAVELENGTH, SATELLITE_VELOCITY
)

from .logger import logger  # noqa: E402

"""
Task.
Draw segments' concentrations.
Obtain trends over concentration parameters of NACS: O, N_2, He, N, Ar.
Note: Since now analysis is provided for NACS solely.

Extension.
Here we're working only with oxygen component of NACS `o_dens`.
Select variation:
1. Identify trend by moving average:
2. De-trend input signal;
3. Perform ideal filtration;
4. Restore signal from spectra;

@TODO: smoother moving average
@TODO: Better ticks:
https://stackoverflow.com/questions/12608788/changing-the-tick-frequency-on-x-or-y-axis-in-matplotlib
"""

# # Signal filtering


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


def tick_labels(value, ticks, precision=2.0):
    value_len = len(value) - 1
    return [
        int(
            value[int(tick * value_len)] * precision
        ) / precision
        for tick in ticks
    ]


# # Original Code


def segments_list(sampling):
    logger.info('{} - listing sampling'.format(sampling))
    sampling_dir = join(ARTIFACTS_DIR, 'samplings', '{:0>3}'.format(sampling))
    return sorted([join(sampling_dir, fname) for fname in listdir(sampling_dir) if fnmatch(fname, '*.asc')])


def omit_zeros(arr):
    arr[arr == 0] = nan
    return arr


def draw_bare(day, hours, lat, legend, density):
    fig = plt.figure()
    ax_ut = fig.add_subplot(111)
    ax_lat = ax_ut.twiny()
    ax_lat.set_xticks(ax_ut.get_xticks())
    ax_lat.set_xticklabels(tick_labels(lat, ax_ut.get_xticks()))
    ax_ut.plot(hours, density)
    ax_ut.legend([legend])
    ax_ut.set(
        xlabel='Day {}, (h)'.format(day),
        ylabel='Density, 1/cm^3',
    )
    ax_lat.set(
        xlabel='Latitude, (deg)'
    )
    title = 'Density of neutral components {} - {}'.format(
        datetime.fromtimestamp(hours[0]).strftime('%Y.%j %H:%M:%S'),
        datetime.fromtimestamp(hours[-1]).strftime('%Y.%j %H:%M:%S')
    )
    ax_ut.set_title(title, y=1.1)
    return fig


def draw_segment(sampling, segment_file):
    logger.info('\t{}: processing'.format(basename(segment_file)))
    segment_data = local_preload(segment_file, FileParser, SampledNACSRow, segment_file)
    ut = segment_data.get('ut', transposed=True)[0]
    lat = segment_data.get('lat', transposed=True)[0]
    o_dens = omit_zeros(segment_data.get('o_dens', transposed=True)[0])

    day, hours = ut_to_hours(ut)

    param_name = 'O density'

    fig_avg, fig_wave = analyze_param(sampling, day, hours, lat, o_dens, param_name)

    fig_avg_artifact_fname = segment_file[:-3] + param_name.lower() + '.trend.png'
    logger.debug('\t\t{}: artifact'.format(basename(fig_avg_artifact_fname)))
    fig_avg.savefig(fig_avg_artifact_fname, dpi=300, papertype='a0', orientation='landscape')
    plt.close(fig_avg)

    fig_wave_artifact_fname = segment_file[:-3] + param_name.lower() + '.wave.png'
    logger.debug('\t\t{}: artifact'.format(basename(fig_wave_artifact_fname)))
    fig_wave.savefig(fig_wave_artifact_fname, dpi=300, papertype='a0', orientation='landscape')
    plt.close(fig_wave)


def smooth_signal(sampling, parameter, window_len=None):
    averaging_segment = 5000  # km
    satellite_velocity = 7.8  # km/s
    if window_len is None:
        window_len = int(averaging_segment // sampling // satellite_velocity)
        window_len += (window_len + 1) % 2  # we make it odd
    return moving_average(parameter, window_len, split_by_nans=True)


def remove_trend(sampling, parameter):
    avg_trend = smooth_signal(sampling, parameter)
    wave = parameter - avg_trend

    signal, fft_trend, noise = ideal_signal_filter(wave, sampling)

    return signal, avg_trend, fft_trend, noise


def ideal_signal_filter(wave, sampling):
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


def data_title(name, day, hours):
    return 'Day {}. {} {:.2f}h - {:.2f}h'.format(day, name, hours[0], hours[-1])


def lat_ticks(lat, precision=2.0):
    lat_i = [(int(lat_v) // precision) * precision for lat_v in lat]
    lat_m = list(sorted(list(set(lat_i))))
    lat_l = len(lat)
    return [lat_i.index(lat_v) / lat_l for lat_v in lat_m]


def hours_ticks(hours):
    hours_i = [int(hour * 50) / 50. for hour in hours]
    return list(sorted(list(set(hours_i))))


def draw_trend(name, day, hours, lat, parameter, avg_trend, fft_trend, noise):
    fig, (ax_hours_trend, ax_hours_noise) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [5, 1]})

    lat_t = lat_ticks(lat)
    hours_m = hours_ticks(hours)

    ax_lat_trend = ax_hours_trend.twiny()
    ax_lat_trend.grid(True, linestyle=':', linewidth=0.5)
    ax_lat_trend.set_xticks(lat_t)
    ax_lat_trend.set_xticklabels(tick_labels(lat, lat_t))
    plt.setp(ax_lat_trend.xaxis.get_majorticklabels(), rotation=-90)
    ax_lat_trend.xaxis.set_tick_params(labelsize=4)

    ax_hours_trend.grid(True, linestyle='-')
    ax_hours_trend.plot(hours, parameter)
    ax_hours_trend.plot(hours, avg_trend)
    ax_hours_trend.plot(hours, fft_trend)
    ax_hours_trend.plot(hours, avg_trend + fft_trend)
    ax_hours_trend.set_xticks(hours_m)
    plt.setp(ax_hours_trend.xaxis.get_majorticklabels(), rotation=-30)
    ax_hours_trend.xaxis.set_tick_params(labelsize=4)
    ax_hours_trend.legend([
        name,
        'MA trend',
        'FFT trend',
        'MA+FFT trend',
    ])
    ax_hours_trend.set_ylabel('Density, 1/cm^3')
    ax_lat_trend.set_xlabel('Latitude, (deg)')

    ax_hours_trend.set_title('{} and avg_trend'.format(data_title(name, day, hours)), y=1.12)

    ax_hours_noise.grid(True)
    ax_hours_noise.plot(hours, noise)
    ax_hours_noise.set_xticks(hours_m)
    plt.setp(ax_hours_noise.xaxis.get_majorticklabels(), rotation=-30)
    ax_hours_noise.xaxis.set_tick_params(labelsize=4)
    ax_hours_noise.set_xlabel('Day {}, (h)'.format(day))

    return fig


def ut_to_hours(uts):
    day_date = datetime.fromtimestamp(uts[0])
    day = day_date.strftime('%Y/%j')
    day_ut = mktime(date(
        int(day_date.strftime('%Y')),
        int(day_date.strftime('%-m')),
        int(day_date.strftime('%-d')),
    ).timetuple())
    return day, array([(ut - day_ut) / 3600. for ut in uts])


def draw_wave(name, day, hours, lat, wave, noise):
    fig, (ax_hours_wave, ax_hours_noise, ax_hours_fft) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [5, 2, 5]})

    lat_t = lat_ticks(lat)
    hours_m = hours_ticks(hours)

    ax_hours_wave.grid(True)

    filler = copy(wave)
    f_nan = isnan(filler)
    fn_nan = ~isnan(filler)
    filler[fn_nan] = nan
    filler[f_nan] = 0

    ax_lat_wave = ax_hours_wave.twiny()
    ax_lat_wave.grid(True, linestyle=':', linewidth=0.5)
    ax_lat_wave.set_xticks(lat_t)
    ax_lat_wave.set_xticklabels(tick_labels(lat, lat_t))
    plt.setp(ax_lat_wave.xaxis.get_majorticklabels(), rotation=-90)
    ax_lat_wave.xaxis.set_tick_params(labelsize=4)
    ax_hours_wave.plot(hours, wave)
    ax_hours_wave.plot(hours, filler, color='red')
    ax_hours_wave.set_xticks(hours_m)
    plt.setp(ax_hours_wave.xaxis.get_majorticklabels(), rotation=-30)
    ax_hours_wave.xaxis.set_tick_params(labelsize=4)
    ax_hours_wave.legend([name, 'Absent data'])
    ax_hours_wave.set(
        ylabel='Density, 1/cm^3',
    )
    ax_lat_wave.set(
        xlabel='Latitude, (deg)'
    )
    ax_hours_wave.set_title('{} wave'.format(data_title(name, day, hours)), y=1.25)

    ax_hours_noise.grid(True)
    ax_hours_noise.plot(hours, noise)
    ax_hours_noise.set_xticks(hours_m)
    plt.setp(ax_hours_noise.xaxis.get_majorticklabels(), rotation=-30)
    ax_hours_noise.xaxis.set_tick_params(labelsize=4)
    ax_hours_noise.set(
        xlabel='Day {}, (h)'.format(day),
    )

    wave[isnan(wave)] = 0  # feel up with zeros for sake of rfft
    ax_hours_fft.plot(array(range(ZEROFILL_LENGTH // 2 + 1)), absolute(rfft(zerofilled_signal(wave))))

    return fig


def analyze_param(sampling, day, hours, lat, parameter, name):
    wave, avg_trend, fft_trend, noise = remove_trend(sampling, parameter)
    return (
        draw_trend(name, day, hours, lat, parameter, avg_trend, fft_trend, noise),
        draw_wave(name, day, hours, lat, wave, noise),
    )


def main():
    for sampling in [1]:  # range(1, 199):
        segments = segments_list(sampling)
        for segment_file in segments:
            draw_segment(sampling, segment_file)


if __name__ == '__main__':
    main()
