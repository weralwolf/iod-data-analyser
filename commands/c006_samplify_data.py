from matplotlib import use as setRenderingBackend  # isort:skip noqa:E402
setRenderingBackend('Agg')  # isort:skip

import json  # noqa:E402
from os import makedirs  # noqa:E402
from os.path import join, basename  # noqa:E402
from datetime import datetime  # noqa:E402

from numpy import concatenate, searchsorted  # noqa:E402
from matplotlib import pyplot as plt  # noqa:E402

from ionospheredata.utils import round, local_preload  # noqa:E402
from ionospheredata.parser import FileParser, FileWriter, SourceNACSRow, SampledNACSRow  # noqa:E402
from ionospheredata.settings import ARTIFACTS_DIR, DE2SOURCE_NACS_DIR  # noqa:E402

from .logger import logger  # noqa: F401, E402


"""
Task.
Generate files with data per-sampling and identify number of continuous tracks and their total length per sampling.
Note: Since now analysis is provided for NACS solely.
"""


def sampling_segments(sampling):
    logger.error('\tCollecting unique longest sampling chunks for {}s'.format(sampling))
    segments_file = join(ARTIFACTS_DIR, 'samplings', '000_splits', 'nacs.{:0>4d}s.sampling.by_ut.json'.format(sampling))
    all_segments = json.load(open(segments_file))
    unintersecting_longest_segments = []
    for segment in all_segments:  # keep in mind that all segments are sorted by segment.0 (by time)
        if len(unintersecting_longest_segments) == 0:
            unintersecting_longest_segments.append(segment)

        elif unintersecting_longest_segments[-1]['segment'][1] < segment['segment'][0]:
            unintersecting_longest_segments.append(segment)

        elif unintersecting_longest_segments[-1]['duration'] < segment['duration']:
            unintersecting_longest_segments[-1] = segment

    return unintersecting_longest_segments


def ut_map(key, dirname, RowParser):
    logger.debug('Computing ut map...')
    datafiles = [join(dirname, fname.strip()) for fname in open(join(ARTIFACTS_DIR, '{}.good.txt'.format(key)), 'r').readlines()]

    # we don't need to keep information about last UT of file, because it is always before next file start
    # and there's no data between end of previous and start of next file
    return[(
        local_preload(fname, FileParser, RowParser, fname).get('ut', transposed=True)[0][0],
        fname,
    ) for fname in sorted(datafiles)]


def enhance_segment(segment, sampling):
    logger.debug('\t\tEnhancing segment {:.0f}-{:.0f}'.format(*segment['segment']))
    from_fields = [
        'ut', 'o_dens', 'o_err', 'n2_dens', 'n2_err', 'he_dens', 'he_err',
        'n_dens', 'n_err', 'ar_dens', 'ar_err', 'orbit', 'alt', 'lat', 'lon',
        'lst', 'lmt', 'l_sh', 'inv_lat', 'sza'
    ]
    uts_boundaries = local_preload('nacs-all-ut', ut_map, 'nacs', DE2SOURCE_NACS_DIR, SourceNACSRow)
    ut_markers = [ut[0] for ut in uts_boundaries]
    ut_refs = dict(uts_boundaries)
    search_boundaries = searchsorted(ut_markers, segment['segment'])
    # @TODO: figure out what is wrong here. Fix bellow is definitely wrong, but I am too tired today.
    search_boundaries = [
        search_boundaries[0] - 1 if search_boundaries[0] > 0 else 0,  # just a quick fix
        search_boundaries[1]
    ]
    logger.debug('\t\t\t{:.0f} : {:.0f} - search gate'.format(*segment['segment']))
    if search_boundaries[1] + 1 not in ut_markers:
        return None
    logger.debug('\t\t\t{} - {}'.format(
        ut_markers[search_boundaries[0]],
        ut_markers[search_boundaries[1] + 1]
    ))
    logger.debug('\t\t\t{} ...{}... {}'.format(
        basename(ut_refs[ut_markers[search_boundaries[0]]]),
        search_boundaries[1] + 1 - search_boundaries[0],
        basename(ut_refs[ut_markers[search_boundaries[1] + 1]])
    ))

    wide_data_context = concatenate([
        local_preload(ut_refs[ut_markers[idx]], FileParser, SourceNACSRow, ut_refs[ut_markers[idx]]).get(*from_fields)
        for idx in range(search_boundaries[0], search_boundaries[1] + 1)
    ])
    logger.debug('\t\t\t{} - wide data length'.format(len(wide_data_context)))
    logger.debug('\t\t\t{:.0f} : {:.0f}'.format(wide_data_context[0][0], wide_data_context[-1][0]))

    narrowed_data_context = wide_data_context[
        (wide_data_context[:, 0] >= segment['segment'][0]) &
        (wide_data_context[:, 0] <= segment['segment'][1])
    ]

    logger.debug('\t\t\t{} - narrow data length'.format(len(narrowed_data_context)))

    sampled_data = []
    last_ut = None
    for row in narrowed_data_context:
        if last_ut is None or round(row[0] - last_ut) == sampling:
            sampled_data.append(row)
            last_ut = row[0]

    logger.debug('\t\t\t{} - sampled data length'.format(len(sampled_data)))

    return sampled_data


def collect_segments(sampling):
    logger.info('{} - assembling data for sampling'.format(sampling))
    segments = sampling_segments(sampling)
    segments_per_day = {}
    sampling_dir = join(ARTIFACTS_DIR, 'samplings', '{:0>3}'.format(sampling))
    makedirs(sampling_dir, exist_ok=True)
    for segment in segments:
        enhanced = enhance_segment(segment, sampling)
        if enhanced is None or len(enhanced) == 0:
            logger.error(json.dumps(segment, indent=2))
            continue
        fw = FileWriter(SampledNACSRow, enhanced)

        segment_start_date = datetime.fromtimestamp(segment['segment'][0])
        day_marker = segment_start_date.strftime('%Y.%j')
        if day_marker not in segments_per_day:
            segments_per_day[day_marker] = 0
        else:
            segments_per_day[day_marker] += 1
        fname = join(sampling_dir, '{}.no{:0>2} - {:.0f} seconds.asc'.format(
            segment_start_date.strftime('%Y.%j'),
            segments_per_day[day_marker],
            enhanced[-1][0] - enhanced[0][0]
        ))
        segment['filename'] = basename(fname)

        logger.info('\t{} - segment file'.format(basename(fname)))
        with open(fname, 'w') as datafile:
            fw.reflect(datafile)

    with open(join(sampling_dir, '000_list.json'), 'w') as segments_list:
        json.dump(segments, segments_list)


def main():
    samplings = [1]  # range(1, 199)
    metrics = []
    for sampling in samplings:
        usegments = sampling_segments(sampling)
        metrics.append((sampling, len(usegments), sum([s['duration'] for s in usegments])))

    x, count, duration = zip(*metrics)
    ax = plt.subplot(211)
    ax.set(
        title='Number of continuous segments per sampling',
        xlabel='Samplings, (s)',
        ylabel='Number of tracks'
    )
    plt.plot(x, count)
    plt.grid(True)

    ax = plt.subplot(212)
    ax.set(
        title='Total duration of continuous segments per sampling',
        xlabel='Samplings, (s)',
        ylabel='Total duration, (s)'
    )
    plt.plot(x, duration)
    plt.grid(True)

    plt.savefig(join(ARTIFACTS_DIR, 'c6.segments_stats.png'), dpi=300, papertype='a0', orientation='landscape')
    plt.clf()

    for sampling in samplings:
        collect_segments(sampling)


if __name__ == '__main__':
    main()
