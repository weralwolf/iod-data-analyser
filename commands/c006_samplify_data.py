from matplotlib import use as setRenderingBackend  # isort:skip noqa:E402
setRenderingBackend('Agg')  # isort:skip

import json  # noqa:E402
from os import listdir, makedirs  # noqa:E402
from fnmatch import fnmatch  # noqa:E402
from os.path import join, basename  # noqa:E402
from commands.utils.logger import logger  # noqa: F401, E402

from numpy import concatenate  # noqa:E402

from ionospheredata.utils import round, local_preload  # noqa:E402
from ionospheredata.parser import FileParser, FileWriter, SourceNACSRow, SampledNACSRow  # noqa:E402
from ionospheredata.settings import ARTIFACTS_DIR, DE2SOURCE_NACS_DIR  # noqa:E402


"""
Task.
Generate files with data per-sampling and identify number of continuous tracks and their total length per sampling.
Note: Since now analysis is provided for NACS solely.
"""


def sampling_segments(sampling):
    logger.error('\tCollecting unique longest sampling chunks for {}s'.format(sampling))
    segments_dir = join(ARTIFACTS_DIR, 'samplings', '000_splits')
    segments_file_tpl = 'nacs.1982*.{:0>4d}s.sampling.by_ut.json'.format(sampling)
    fnames = [
        fname
        for fname in listdir(segments_dir)
        if fnmatch(fname, segments_file_tpl)
    ]
    for fname in sorted(fnames):
        yield fname[5:12], json.load(open(join(segments_dir, fname)))


all_datafiles = [
    fname.strip()
    for fname in open(join(ARTIFACTS_DIR, '{}.good.txt'.format('nacs')), 'r').readlines()
]


def enhance_segment(day, segment, sampling):
    logger.debug('\t\tEnhancing segment {:.0f}-{:.0f}'.format(*segment['segment']))
    from_fields = [
        'ut_of_day', 'o_dens', 'o_err', 'n2_dens', 'n2_err', 'he_dens', 'he_err',
        'n_dens', 'n_err', 'ar_dens', 'ar_err', 'orbit', 'alt', 'lat', 'lon',
        'lst', 'lmt', 'l_sh', 'inv_lat', 'sza'
    ]

    datafiles = sorted([join(DE2SOURCE_NACS_DIR, fname) for fname in all_datafiles if fname.startswith(day)])

    wide_data_context = concatenate([
        local_preload(fname, FileParser, SourceNACSRow, fname).get(*from_fields)
        for fname in datafiles
    ])

    return wide_data_context[
        (wide_data_context[:, 0] >= segment['segment'][0] * 1000) &
        (wide_data_context[:, 0] <= segment['segment'][1] * 1000)
    ]


def collect_segments(sampling):
    logger.info('{} - assembling data for sampling'.format(sampling))
    sampling_dir = join(ARTIFACTS_DIR, 'samplings', '{:0>3}'.format(sampling))
    makedirs(sampling_dir, exist_ok=True)

    for day, segments in sampling_segments(sampling):
        for segment_idx, segment in enumerate(segments):
            enhanced = enhance_segment(day, segment, sampling)
            if enhanced is None or len(enhanced) == 0:
                logger.error(json.dumps(segment, indent=2))
                continue

            fw = FileWriter(SampledNACSRow, enhanced)
            fname = join(sampling_dir, '{}.no{:0>2} - {:.0f} seconds.asc'.format(
                day,
                segment_idx,
                round((enhanced[-1][0] - enhanced[0][0]) / 1000)
            ))
            segment['filename'] = basename(fname)

            logger.info('\t{} - segment file'.format(basename(fname)))
            with open(fname, 'w') as datafile:
                fw.reflect(datafile)

        with open(join(sampling_dir, '000.{}_list.json'.format(day)), 'w') as segments_list:
            json.dump(segments, segments_list)


def main():
    samplings = [1]  # range(1, 199)
    for sampling in samplings:
        collect_segments(sampling)


if __name__ == '__main__':
    main()
