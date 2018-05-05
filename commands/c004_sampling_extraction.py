import json
from math import sqrt
from os.path import join, exists

from numpy import array, concatenate

from ionospheredata.utils import round, local_preload
from ionospheredata.parser import FileParser, SourceNACSRow, SourceWATSRow
from ionospheredata.settings import ARTIFACTS_DIR, DE2SOURCE_NACS_DIR, DE2SOURCE_WATS_DIR

from .logger import logger


"""
Task.
Identify continous sections of data in fixed sampling in range [2s, ~200s].
"""


def chunkup(data):
    chunks = []
    # Lets ignore fluctuations of sampling within 1s
    for datafile in data:
        ut = datafile.get('ut', transposed=True)[0]
        ongoing_sampling = round(ut[1] - ut[0])  # We're sure there's no files with less than 2 datapoints
        starts_at = 0
        for idx in range(1, len(ut)):
            sampling = round(ut[idx] - ut[idx - 1])
            if sampling == ongoing_sampling:
                continue

            chunks.append((
                ut[starts_at],
                ut[idx - 1],
                idx - starts_at,
                ongoing_sampling
            ))
            starts_at = idx - 1
            ongoing_sampling = sampling

        chunks.append((
            ut[starts_at],
            ut[-1],
            len(ut) - starts_at,
            ongoing_sampling
        ))
    for n, (start, end, length, sampling) in enumerate(chunks):
        logger.info('{}.\t{}\t- {}\t{} / {}'.format(n, start, end, sampling, length))

    return chunks


def verify_sampling(deltas, sampling):
    match = 0
    points = 0
    for idx in range(0, len(deltas)):
        if match == sampling:
            points += 1
            match = 0
        elif match > sampling:
            return None
        match += deltas[idx]
    else:
        return points + int(match == sampling)


def artifacts(key, sampling):
    return (
        join(ARTIFACTS_DIR, 'samplings', '000_splits', '{}.{:0>4d}s.sampling.by_ut.json'.format(key, sampling)),
        join(ARTIFACTS_DIR, 'samplings', '000_splits', '{}.{:0>4d}s.sampling.by_length.json'.format(key, sampling))
    )


def make_deltas(key, dirname, RowParser):
    logger.info('{}. Reading datafiles'.format(key))
    datafiles = [join(dirname, fname.strip()) for fname in open(join(ARTIFACTS_DIR, '{}.good.txt'.format(key)), 'r').readlines()]
    ut = concatenate([
        local_preload(fname, FileParser, RowParser, fname).get('ut', transposed=True)[0]
        for fname in sorted(datafiles)
    ], axis=0)
    deltas = []
    logger.info('{}. Compute deltas'.format(key))
    logger.info('{}: total keys'.format(len(ut)))
    deltas = (concatenate([ut, array([0])]) - concatenate([array([0]), ut]))[1:]
    return deltas, ut


def sample(key, dirname, RowParser, sampling):
    deltas, ut = local_preload('{}-deltas'.format(key), make_deltas, key, dirname, RowParser)
    logger.info(deltas)

    # 1. Split on chunks with gaps no longer than sampling;
    # 2. Iterate over datashifts 0 <= j < sampling;
    # 3. Look for sampling matches;
    # 4. Exclude multiples of matched samplings;
    # 5. Store (t_start, t_end, sampling) taking in acount sampling shift j;

    logger.info('{}: Total length of ut'.format(len(ut)))
    min_sequence_duration = 250 * sqrt(sampling)
    working_samplings = []
    logger.info('{}: sampling to check'.format(sampling))
    starts_at = 0
    for idx in range(len(deltas)):
        if deltas[idx] > sampling and ut[idx] - ut[starts_at] > min_sequence_duration:
            printed = False
            shift = 0
            while sum(deltas[starts_at:starts_at + shift]) < sampling:
                points = verify_sampling(deltas[starts_at + shift:idx], sampling)
                if points is not None and points > 0:
                    if not printed:
                        logger.info('\t{} - {}'.format(ut[starts_at], ut[idx]))
                        printed = True
                    logger.info('\t\t+{} / {}: shift / sampling'.format(shift, sampling))
                    working_samplings.append({
                        'indexes': (starts_at + shift, idx),
                        'length': idx - starts_at - shift + 1,
                        'points': points,
                        'segment': (ut[starts_at + shift], ut[idx]),
                        'duration': ut[idx] - ut[starts_at + shift],
                        'resolution': float(sampling) / points,
                    })
                shift += 1
            starts_at = idx + 1

    by_ut, by_length = artifacts(key, sampling)

    with open(by_ut, 'w') as artifact:
        json.dump(working_samplings, artifact)

    with open(by_length, 'w') as artifact:
        json.dump(sorted(
            working_samplings,
            key=lambda x: (-x['duration'], x['segment'][0])
        ), artifact)


def chunkup_samplings(key, dirname, RowParser):
    for sampling in range(2, round(1700 / 8.6) + 1):  # No gap longer than 1700km
        by_ut, by_length = artifacts(key, sampling)
        if not exists(by_ut) or not exists(by_length):
            sample(key, dirname, RowParser, sampling)


def main():
    chunkup_samplings('nacs', DE2SOURCE_NACS_DIR, SourceNACSRow)
    chunkup_samplings('wats', DE2SOURCE_WATS_DIR, SourceWATSRow)


if __name__ == '__main__':
    main()
