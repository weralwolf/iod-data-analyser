from os.path import join, basename

from iod.a000_config import DE2_NACS_DIR, DE2_WATS_DIR, ARTEFACTS_DIR
from ionospheredata.utils import local_preload, list_datafiles
from ionospheredata.parser import NACSRow, WATSRow, FileParser


def check_ut_monotone(filename, RowParser):
    filedata = local_preload(filename, FileParser, RowParser, filename)
    uts = filedata.get('ut_of_day', transposed=True)[0]
    for idx in range(1, len(uts)):
        if uts[idx] <= uts[idx - 1]:
            return False
    return True


def bad_files(RowParser, dirname):
    bads = []
    datafiles = list_datafiles(dirname)
    for idx, filename in enumerate(datafiles):
        if not check_ut_monotone(filename, RowParser):
            # print("{} BAD ... {}".format(idx, filename))
            bads.append(filename)
    return bads


def data_report(key, RowParser, dirname):
    # bad_datafiles = local_preload('{}_bad_files'.format(key), bad_files, RowParser, dirname)
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
        print("{}. {}".format(n, file_key))
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
                print("\t[{}/{}] {} > {}".format(idx, len(uts), uts[idx - 1], uts[idx]))

                if breaking_idx == -1:  # We care about very first data compromising datapoint
                    breaking_idx = idx - 1

        if file_name in doppelganger_class or file_name in midnightcut_class:
            badfiles_datapoints += len(filedata.data)
            good_datapoints_in_badfiles += breaking_idx + 1  # + 0th index

    jumps_histogram = {k: len(list(filter(lambda x: len(x) == k, jumps_per_file.values()))) for k in set([len(x) for x in jumps_per_file.values()])}
    all_badfiles = list(midnightcut_class) + list(doppelganger_class)
    print("key: {}".format(key.upper()))
    print("\tTotals:")
    print("\t{}: total data points".format(total_datapoints))
    print("\t\t{}: total data points in bad files".format(badfiles_datapoints))
    print("\t\t{:2.4}%: % of all datapoints in bad files".format(100. * badfiles_datapoints / total_datapoints))
    print("\t\t{}: total good datapoints in BAD files".format(good_datapoints_in_badfiles))
    print("\t\t{}: total good datapoints in ALL files".format(total_datapoints - badfiles_datapoints + good_datapoints_in_badfiles))
    print("\t\t{:2.4}%: ratio of good datapoints to all datapoints".format(100. - 100 * (badfiles_datapoints - good_datapoints_in_badfiles) / total_datapoints))
    print("\t{}: total data files".format(total_files))
    print("\t{}: total bad files".format(len(all_badfiles)))
    print("\t\t{}: midnight cut".format(len(midnightcut_class)))
    for jumps, files in jumps_histogram.items():
        print("\t\t\t{} jumps in {} files".format(jumps, files))
    print("\t\t{}: doppelgangers".format(len(doppelganger_class)))
    print("\t\t\t{}: of them in the end of file".format(dc_eof))
    print("\t\t\t{}: of them NOT in the end of file".format(dc_neof))
    print("\t{:2.4}%: rate of losts with removing doppledangers".format(100 * (dc_eof + dc_neof) / total_datapoints))
    print("Bad files:")
    for badfile_name in sorted(all_badfiles):
        print("\t\t{}".format(basename(badfile_name)))

    with open(join(ARTEFACTS_DIR, "{}.notmonotone.txt".format(key)), 'w') as datafile:
        datafile.write("\n".join([basename(filename) for filename in all_badfiles]))


if __name__ == '__main__':
    nacs_badfiles = data_report('nacs', NACSRow, DE2_NACS_DIR)
    wats_badfiles = data_report('wats', WATSRow, DE2_WATS_DIR)
