import hashlib
from os.path import join, basename

from iod.a000_config import DE2_NACS_DIR, DE2_WATS_DIR, ARTEFACTS_DIR
from ionospheredata.utils import local_preload, list_datafiles
from ionospheredata.parser import NACSRow, WATSRow, FileParser


def read_badfileslist(basedir, filename):
    return [join(basedir, badfilename.strip()) for badfilename in open(filename).readlines()]


def goodfiles(basedir, badfiles):
    return [fname for fname in list_datafiles(basedir) if fname not in badfiles]


def dataof(filename):
    return open(filename, 'r').read()


def find_duplicates(filenames):
    hashes = {}
    for filename in filenames:
        fhash = hashlib.sha256(dataof(filename).encode('utf-8').strip()).hexdigest()
        if fhash not in hashes:
            hashes[fhash] = []
        hashes[fhash].append(filename)

    for fhash, fnames in hashes.items():
        if len(fnames) < 2:
            continue
        print("\n\t{}".format(fhash))
        for fname in fnames:
            print("\t\t{}".format(basename(fname)))

    return {ec[0] for ec in hashes.values() if len(ec) > 1}


def find_intersections(filenames, RowParser):
    filenames = sorted(filenames)
    intersected = []
    for idx in range(1, len(filenames)):
        pdata = local_preload(filenames[idx - 1], FileParser, RowParser, filenames[idx - 1]).get('ut', transposed=True)[0]
        cdata = local_preload(filenames[idx], FileParser, RowParser, filenames[idx]).get('ut', transposed=True)[0]
        if pdata[-1] > cdata[0]:
            intersected.append([filenames[idx - 1], filenames[idx]])
            # print("{} & {}\n\t{} > {}".format(basename(filenames[idx - 1]), basename(filenames[idx]), pdata[-1], cdata[0]))

    return set(sum(intersected, []))


def filtration(key, basedir, RowParser):
    badfiles = read_badfileslist(
        basedir,
        join(ARTEFACTS_DIR, '{}.notmonotone.txt'.format(key.upper()))
    )
    datafiles = goodfiles(basedir, badfiles)
    print("key: {}".format(key.upper()))
    print("\t{}: total number of good datafiles".format(len(datafiles)))
    duplicates = find_duplicates(datafiles)
    filtered_datafiles = list(set(datafiles).difference(duplicates))
    print("\t{}: total number of exclusive datafiles".format(len(filtered_datafiles)))
    total_intersections_list = []
    iteration_number = 0
    while True:
        intersections = find_intersections(filtered_datafiles, RowParser)
        print("\t{} iteration. Intersection search".format(iteration_number))
        iteration_number += 1
        print("\t\t{} files are intersecting".format(len(intersections)))
        if len(intersections) == 0:
            break
        total_intersections_list += list(intersections)
        filtered_datafiles = list(set(filtered_datafiles).difference(intersections))

    print("{} files left after filtering".format(len(filtered_datafiles)))
    total_datapoints = sum([
        len(local_preload(filename, FileParser, RowParser, filename).get('ut', transposed=True)[0])
        for filename in filtered_datafiles
    ])
    print("{} datapoints left".format(total_datapoints))
    print("\nDuplicated files:")
    for fname in duplicates:
        print("\t{}".format(basename(fname)))

    with open(join(ARTEFACTS_DIR, '{}.duplicates.txt'.format(key.upper())), 'w') as datafile:
        datafile.writelines([basename(filename) for filename in sorted(duplicates)])

    print("\nIntersected files:")
    for fname in total_intersections_list:
        print("\t{}".format(basename(fname)))

    with open(join(ARTEFACTS_DIR, '{}.intersections.txt'.format(key.upper())), 'w') as datafile:
        datafile.writelines([basename(filename) for filename in sorted(intersections)])

    with open(join(ARTEFACTS_DIR, '{}.ignore.txt'.format(key.upper())), 'w') as datafile:
        datafile.writelines([basename(filename) for filename in sorted(badfiles)])
        datafile.writelines([basename(filename) for filename in sorted(intersections)])
        datafile.writelines([basename(filename) for filename in sorted(duplicates)])

    with open(join(ARTEFACTS_DIR, '{}.good.txt'.format(key.upper())), 'w') as datafile:
        datafile.writelines([basename(filename) for filename in sorted(datafiles)])


if __name__ == "__main__":
    filtration("nacs", DE2_NACS_DIR, NACSRow)
    filtration("wats", DE2_WATS_DIR, WATSRow)
