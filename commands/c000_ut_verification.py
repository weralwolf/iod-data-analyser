from os.path import join, basename
from commands.parsers import FileParser, SourceNACSRow, SourceWATSRow
from commands.utils.logger import logger

from ionospheredata.utils import local_preload, list_datafiles
from ionospheredata.settings import ARTIFACTS_DIR, DE2SOURCE_NACS_DIR, DE2SOURCE_WATS_DIR


"""
Task.
Identify "good" data files as those we don't need to fix before usage. From investigation it is clear that
there's a two types of problems each file can have inside:
1. UT jumps: when ut behaves not monotonically;
2. UT duplicates: when ut records have duplicates next to them;
"""


def data_report(key, RowParser, dirname):
    datafiles = list_datafiles(dirname)
    doppelganger_class = set()
    dc_eof = 0  # usually doppleganers appears at the end of the file, but better check it
    dc_neof = 0
    midnightcut_class = set()
    jumps_per_file = {}
    total_datapoints = 0
    badfiles_datapoints = 0
    good_datapoints_in_badfiles = 0
    total_files = len(list_datafiles(dirname))
    for n, file_name in enumerate(datafiles):
        breaking_idx = -1
        file_key = basename(file_name)
        logger.debug('{}. {}'.format(n, file_key))
        filedata = local_preload(file_name, FileParser, RowParser, file_name)
        uts = filedata.get('ut_of_day', transposed=True)[0]
        total_datapoints += len(filedata.data)
        for idx in range(1, len(uts)):
            if uts[idx] == uts[idx - 1]:
                doppelganger_class.add(file_name)
                if idx + 1 == len(uts):
                    dc_eof += 1
                else:
                    dc_neof += 1
                if breaking_idx == -1:  # We care about very first data compromising datapoint
                    breaking_idx = idx - 2  # Because we count both of dopplegangers as bad datapoints

            if uts[idx] < uts[idx - 1]:
                midnightcut_class.add(file_name)

                if file_key not in jumps_per_file:
                    jumps_per_file[file_key] = list()
                jumps_per_file[file_key].append((uts[idx - 1], uts[idx]))
                logger.debug('\t[{}/{}] {} > {}'.format(idx, len(uts), uts[idx - 1], uts[idx]))

                if breaking_idx == -1:  # We care about very first data compromising datapoint
                    breaking_idx = idx - 1

        if file_name in doppelganger_class or file_name in midnightcut_class:
            badfiles_datapoints += len(filedata.data)
            good_datapoints_in_badfiles += breaking_idx + 1  # + 0th index

    jumps_histogram = {k: len(list(filter(lambda x: len(x) == k, jumps_per_file.values()))) for k in set([len(x) for x in jumps_per_file.values()])}
    all_badfiles = list(midnightcut_class) + list(doppelganger_class)
    logger.info('key: {}'.format(key))
    logger.info('\tTotals:')
    logger.info('\t{}: total data points'.format(total_datapoints))
    logger.info('\t\t{}: total data points in bad files'.format(badfiles_datapoints))
    logger.info('\t\t{:2.4}%: % of all datapoints in bad files'.format(100. * badfiles_datapoints / total_datapoints))
    logger.info('\t\t{}: total good datapoints in BAD files'.format(good_datapoints_in_badfiles))
    logger.info('\t\t{}: total good datapoints in ALL files'.format(total_datapoints - badfiles_datapoints + good_datapoints_in_badfiles))
    logger.info('\t\t{:2.4}%: ratio of good datapoints to all datapoints'.format(
        100. - 100 * (badfiles_datapoints - good_datapoints_in_badfiles) / total_datapoints)
    )
    logger.info('\t{}: total data files'.format(total_files))
    logger.info('\t{}: total bad files'.format(len(all_badfiles)))
    logger.info('\t\t{}: midnight cut'.format(len(midnightcut_class)))
    for jumps, files in jumps_histogram.items():
        logger.info('\t\t\t{} jumps in {} files'.format(jumps, files))
    logger.info('\t\t{}: doppelgangers'.format(len(doppelganger_class)))
    logger.info('\t\t\t{}: of them in the end of file'.format(dc_eof))
    logger.info('\t\t\t{}: of them NOT in the end of file'.format(dc_neof))
    logger.info('\t{:2.4}%: rate of losts with removing doppledangers'.format(100 * (dc_eof + dc_neof) / total_datapoints))
    logger.debug('Bad files:')
    for badfile_name in sorted(all_badfiles):
        logger.debug('\t\t{}'.format(basename(badfile_name)))

    with open(join(ARTIFACTS_DIR, '{}.notmonotone.txt'.format(key)), 'w') as datafile:
        datafile.write('\n'.join([basename(filename) for filename in all_badfiles]))


def main():
    data_report('nacs', SourceNACSRow, DE2SOURCE_NACS_DIR)
    data_report('wats', SourceWATSRow, DE2SOURCE_WATS_DIR)


if __name__ == '__main__':
    main()
