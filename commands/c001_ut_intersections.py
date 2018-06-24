import hashlib
from os.path import join, basename
from commands.parsers import FileParser, SourceNACSRow, SourceWATSRow
from commands.utils.logger import logger

from ionospheredata.utils import local_preload, list_datafiles
from ionospheredata.settings import ARTIFACTS_DIR, DE2SOURCE_NACS_DIR, DE2SOURCE_WATS_DIR


"""
Task.
Identify files where UT records overlapping between files. For simplicity both files are removed,
except cases when content of both files exactly identical. In case of identical files only one
is going to be trashed.
"""


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
        logger.info('\n\t{}'.format(fhash))
        for fname in fnames:
            logger.info('\t\t{}'.format(basename(fname)))

    return {ec[0] for ec in hashes.values() if len(ec) > 1}


def find_intersections(filenames, RowParser):
    filenames = sorted(filenames)
    intersected = []
    for idx in range(1, len(filenames)):
        pdata = local_preload(filenames[idx - 1], FileParser, RowParser, filenames[idx - 1]).get('ut', transposed=True)[0]
        cdata = local_preload(filenames[idx], FileParser, RowParser, filenames[idx]).get('ut', transposed=True)[0]
        if pdata[-1] > cdata[0]:
            intersected.append([filenames[idx - 1], filenames[idx]])
            # logger.info('{} & {}\n\t{} > {}'.format(basename(filenames[idx - 1]), basename(filenames[idx]), pdata[-1], cdata[0]))

    return set(sum(intersected, []))


def filtration(key, basedir, RowParser):
    badfiles = read_badfileslist(
        basedir,
        join(ARTIFACTS_DIR, '{}.notmonotone.txt'.format(key))
    )
    datafiles = goodfiles(basedir, badfiles)
    logger.info('key: {}'.format(key))
    logger.info('\t{}: total number of good datafiles'.format(len(datafiles)))
    duplicates = find_duplicates(datafiles)
    filtered_datafiles = list(set(datafiles).difference(duplicates))
    logger.info('\t{}: total number of exclusive datafiles'.format(len(filtered_datafiles)))
    total_intersections_list = []
    iteration_number = 0
    while True:
        intersections = find_intersections(filtered_datafiles, RowParser)
        logger.info('\t{} iteration. Intersection search'.format(iteration_number))
        iteration_number += 1
        logger.info('\t\t{} files are intersecting'.format(len(intersections)))
        if len(intersections) == 0:
            break
        total_intersections_list += list(intersections)
        filtered_datafiles = list(set(filtered_datafiles).difference(intersections))

    logger.info('{} files left after filtering'.format(len(filtered_datafiles)))
    total_datapoints = sum([
        len(local_preload(filename, FileParser, RowParser, filename).get('ut', transposed=True)[0])
        for filename in filtered_datafiles
    ])
    logger.info('{} datapoints left'.format(total_datapoints))
    logger.info('\nDuplicated files:')
    for fname in duplicates:
        logger.info('\t{}'.format(basename(fname)))

    with open(join(ARTIFACTS_DIR, '{}.duplicates.txt'.format(key)), 'w') as datafile:
        datafile.write('\n'.join([basename(filename) for filename in sorted(duplicates)]))

    logger.info('\nIntersected files:')
    for fname in total_intersections_list:
        logger.info('\t{}'.format(basename(fname)))

    with open(join(ARTIFACTS_DIR, '{}.intersections.txt'.format(key)), 'w') as datafile:
        datafile.write('\n'.join([basename(filename) for filename in sorted(intersections)]))

    with open(join(ARTIFACTS_DIR, '{}.ignore.txt'.format(key)), 'w') as datafile:
        datafile.write('\n'.join([basename(filename) for filename in sorted(list(badfiles) + list(intersections) + list(duplicates))]))

    with open(join(ARTIFACTS_DIR, '{}.good.txt'.format(key)), 'w') as datafile:
        datafile.write('\n'.join([basename(filename) for filename in sorted(datafiles)]))


def main():
    filtration('nacs', DE2SOURCE_NACS_DIR, SourceNACSRow)
    filtration('wats', DE2SOURCE_WATS_DIR, SourceWATSRow)


if __name__ == '__main__':
    main()
