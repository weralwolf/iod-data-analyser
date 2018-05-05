from matplotlib import use as setRenderingBackend  # isort:skip noqa:E402
setRenderingBackend('Agg')  # isort:skip

from os import listdir  # noqa: E402
from fnmatch import fnmatch  # noqa: E402
from os.path import join, basename  # noqa: E402
from datetime import datetime  # noqa: E402

from numpy import nan  # noqa: E402
from matplotlib import pyplot as plt  # noqa: E402

from ionospheredata.utils import local_preload  # noqa: E402
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
    sampling_dir = join(ARTIFACTS_DIR, 'samplings', '{:0>3}'.format(sampling))
    return sorted([join(sampling_dir, fname) for fname in listdir(sampling_dir) if fnmatch(fname, '*.asc')])


def omit_zeros(arr):
    arr[arr == 0] = nan
    return arr


def draw_segment(segment_file):
    # @TODO: filter out zeros of concentration for drawing
    logger.info('Processing: {}'.format(basename(segment_file)))
    segment_data = local_preload(segment_file, FileParser, SampledNACSRow, segment_file)
    ut = segment_data.get('ut', transposed=True)[0]
    o_dens = omit_zeros(segment_data.get('o_dens', transposed=True)[0])
    n2_dens = omit_zeros(segment_data.get('n2_dens', transposed=True)[0])
    he_dens = omit_zeros(segment_data.get('he_dens', transposed=True)[0])
    n_dens = omit_zeros(segment_data.get('n_dens', transposed=True)[0])
    ar_dens = omit_zeros(segment_data.get('ar_dens', transposed=True)[0])

    plt.plot(ut, o_dens)
    plt.plot(ut, n2_dens)
    plt.plot(ut, he_dens)
    plt.plot(ut, n_dens)
    plt.plot(ut, ar_dens)
    plt.legend([
        'O density',
        'N2 density',
        'He density',
        'N density',
        'Ar density'
    ])
    plt.xlabel('Universal time, (s)')
    plt.ylabel('Density, 1/cm^3')
    plt.title('Density of neutral components {} - {}'.format(
        datetime.fromtimestamp(ut[0]).strftime('%Y.%j %H:%M:%S'),
        datetime.fromtimestamp(ut[-1]).strftime('%Y.%j %H:%M:%S')
    ))
    artefact_fname = segment_file[:-3] + 'png'
    logger.debug('\t artefact: {}'.format(basename(artefact_fname)))
    plt.savefig(artefact_fname, dpi=300, papertype='a0', orientation='landscape')
    plt.clf()


def main():
    segments = segments_list(2)
    for segment_file in segments:
        draw_segment(segment_file)


if __name__ == '__main__':
    main()
