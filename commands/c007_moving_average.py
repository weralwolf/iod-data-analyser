from matplotlib import use as setRenderingBackend  # isort:skip noqa:E402
setRenderingBackend('Agg')  # isort:skip

from os import listdir  # noqa: E402
from fnmatch import fnmatch  # noqa: E402
from os.path import join, basename  # noqa: E402
from datetime import datetime  # noqa: E402

from numpy import nan, isnan, absolute  # noqa: E402
from numpy.fft import rfft, rfftfreq  # noqa: E402
from matplotlib import pyplot as plt  # noqa: E402

from ionospheredata.utils import local_preload  # noqa: E402
from ionospheredata.method import moving_average  # noqa: E402
from ionospheredata.parser import FileParser, SampledNACSRow  # noqa: E402
from ionospheredata.settings import ARTIFACTS_DIR  # noqa: E402

from .logger import logger  # noqa: E402


"""
Task.
Draw segments' concentrations.
Obtain trends over concentration parameters of NACS: O, N_2, He, N, Ar.
Note: Since now analysis is provided for NACS solely.
"""


def segments_list(sampling):
    logger.info('{} - listing sampling'.format(sampling))
    sampling_dir = join(ARTIFACTS_DIR, 'samplings', '{:0>3}'.format(sampling))
    return sorted([join(sampling_dir, fname) for fname in listdir(sampling_dir) if fnmatch(fname, '*.asc')])


def omit_zeros(arr):
    arr[arr == 0] = nan
    return arr


def draw_bare(ut, alt, params):
    fig = plt.figure()
    ax_ut = fig.add_subplot(111)
    ax_alt = ax_ut.twiny()
    ax_alt.set_xticks(ax_ut.get_xticks())
    ax_alt.set_xticklabels(alt)
    legend, densities = zip(*params)
    for dens in densities:
        ax_ut.plot(ut, dens)
    ax_ut.legend(legend)
    ax_ut.set(
        xlabel='Universal time, (s)',
        ylabel='Density, 1/cm^3',
    )
    ax_alt.set(
        xlabel='Altitude, (km)'
    )
    title = 'Density of neutral components {} - {}'.format(
        datetime.fromtimestamp(ut[0]).strftime('%Y.%j %H:%M:%S'),
        datetime.fromtimestamp(ut[-1]).strftime('%Y.%j %H:%M:%S')
    )
    ax_ut.set_title(title, y=1.1)
    return fig


def draw_segment(sampling, segment_file):
    logger.info('\t{}: processing'.format(basename(segment_file)))
    segment_data = local_preload(segment_file, FileParser, SampledNACSRow, segment_file)
    ut = segment_data.get('ut', transposed=True)[0]
    alt = segment_data.get('alt', transposed=True)[0]
    o_dens = omit_zeros(segment_data.get('o_dens', transposed=True)[0])
    n2_dens = omit_zeros(segment_data.get('n2_dens', transposed=True)[0])
    he_dens = omit_zeros(segment_data.get('he_dens', transposed=True)[0])
    n_dens = omit_zeros(segment_data.get('n_dens', transposed=True)[0])
    ar_dens = omit_zeros(segment_data.get('ar_dens', transposed=True)[0])

    params = [
        ('O density', o_dens),
        ('N2 density', n2_dens),
        ('He density', he_dens),
        ('N density', n_dens),
        ('Ar density', ar_dens),
    ]

    bare_fig = draw_bare(ut, alt, params)

    artifact_fname = segment_file[:-3] + 'png'
    logger.debug('\t\t{}: artifact'.format(basename(artifact_fname)))
    bare_fig.savefig(artifact_fname, dpi=300, papertype='a0', orientation='landscape')
    plt.close(bare_fig)

    for name, param in params:
        fig_avg, fig_wave = analyze_param(sampling, ut, alt, param, name)

        fig_avg_artifact_fname = segment_file[:-3] + name.lower() + '.trend.png'
        logger.debug('\t\t{}: artifact'.format(basename(fig_avg_artifact_fname)))
        fig_avg.savefig(fig_avg_artifact_fname, dpi=300, papertype='a0', orientation='landscape')
        plt.close(fig_avg)

        fig_wave_artifact_fname = segment_file[:-3] + name.lower() + '.wave.png'
        logger.debug('\t\t{}: artifact'.format(basename(fig_wave_artifact_fname)))
        fig_wave.savefig(fig_wave_artifact_fname, dpi=300, papertype='a0', orientation='landscape')
        plt.close(fig_wave)


def remove_trend(sampling, parameter):
    averaging_segment = 5000  # km
    satellite_velocity = 8.6  # km/s
    window_len = int(averaging_segment // sampling // satellite_velocity)
    window_len += (window_len + 1) % 2  # we make it odd
    avg_trend = moving_average(parameter, window_len, split_by_nans=True)
    return parameter - avg_trend, avg_trend


def data_title(name, ut):
    return '{} {} - {}'.format(
        name,
        datetime.fromtimestamp(ut[0]).strftime('%Y.%j %H:%M:%S'),
        datetime.fromtimestamp(ut[-1]).strftime('%Y.%j %H:%M:%S')
    )


def draw_trend(name, ut, alt, parameter, trend):
    fig = plt.figure()
    ax_ut = fig.add_subplot(111)
    ax_alt = ax_ut.twiny()
    ax_alt.set_xticks(ax_ut.get_xticks())
    ax_alt.set_xticklabels(alt)
    ax_ut.plot(ut, parameter)
    ax_ut.plot(ut, trend)
    ax_ut.legend([
        name,
        'Moving average'
    ])
    ax_ut.set(
        xlabel='Universal time, (s)',
        ylabel='Density, 1/cm^3',
    )
    ax_alt.set(
        xlabel='Altitude, (km)'
    )

    ax_ut.set_title('{} and trend'.format(data_title(name, ut)), y=1.1)

    return fig


def draw_wave(name, sampling, ut, alt, wave):
    fig = plt.figure()

    wave[isnan(wave)] = 0  # feel up with zeros for sake of rfft

    # Drawing wave
    ax_ut = fig.add_subplot(211)
    ax_alt = ax_ut.twiny()
    ax_alt.set_xticks(ax_ut.get_xticks())
    ax_alt.set_xticklabels(alt)
    ax_ut.plot(ut, wave)
    ax_ut.legend([name])
    ax_ut.set(
        xlabel='Universal time, (s)',
        ylabel='Density, 1/cm^3',
    )
    ax_alt.set(
        xlabel='Altitude, (km)'
    )
    ax_ut.set_title('{} wave'.format(data_title(name, ut)), y=1.1)

    # Drawing rfft
    ax_ut = fig.add_subplot(212)
    ax_ut.plot(rfftfreq(len(wave), 1. / sampling), absolute(rfft(wave)))
    ax_ut.set(
        xlabel='Frequency, (Hz)',
        # ylabel='Density, 1/cm^3',
    )

    return fig


def analyze_param(sampling, ut, alt, parameter, name):
    wave, trend = remove_trend(sampling, parameter)
    return (
        draw_trend(name, ut, alt, parameter, trend),
        draw_wave(name, sampling, ut, alt, wave),
    )


def main():
    for sampling in range(2, 199):
        segments = segments_list(sampling)[:3]
        for segment_file in segments:
            draw_segment(sampling, segment_file)


if __name__ == '__main__':
    main()
