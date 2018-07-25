import json
from math import sqrt
from os.path import join
from datetime import date
from commands.utils import chalk
from commands.parsers import FileParser, SourceNACSRow
from commands.utils.logger import logger

from numpy import abs, array, isnan, round, concatenate

from ionospheredata.utils import local_preload
from ionospheredata.settings import ARTIFACTS_DIR, DE2SOURCE_NACS_DIR


"""
Task.
Identify continous sections of data in fixed sampling in range [2s, ~200s].
@TODO: Also specify parameters by presence of which identify continuity of a time point.
"""


def chunkup(data):
    chunks = []
    # Lets ignore fluctuationsx of sampling within 1s
    for datafile in data:
        ut = datafile.get('ut_of_day', transposed=True)[0]
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
        if abs(match - sampling) <= 0.5:
            points += 1
            match = 0
        elif match - sampling >= 0.5:
            return None
        match += deltas[idx]
    else:
        return points + int(match == sampling)


def artifacts(day, key, sampling):
    return (
        join(ARTIFACTS_DIR, 'samplings', '000_splits', '{}.{}.{:0>4d}s.sampling.by_ut.json'.format(key, day, sampling)),
        join(ARTIFACTS_DIR, 'samplings', '000_splits', '{}.{}.{:0>4d}s.sampling.by_length.json'.format(key, day, sampling))
    )


def make_deltas(key, dirname, RowParser):
    logger.info('{}. Reading datafiles'.format(key))
    all_datafiles = [
        fname.strip()
        for fname in open(join(ARTIFACTS_DIR, '{}.good.txt'.format(key)), 'r').readlines()
    ]

    days = {fname[:7] for fname in all_datafiles}

    for day in days:
        datafiles = sorted([join(dirname, fname) for fname in all_datafiles if fname.startswith(day)])
        ut = round(concatenate([
            local_preload(fname, FileParser, RowParser, fname).get('ut_of_day', transposed=True)[0]
            for fname in datafiles
        ], axis=0) / 1000.)

        o_dens = concatenate([
            local_preload(fname, FileParser, RowParser, fname).get('o_dens', transposed=True)[0]
            for fname in datafiles
        ], axis=0)

        deltas = (concatenate([ut, array([0])]) - concatenate([array([0]), ut]))[1:]
        yield day, deltas, ut, o_dens


def sample(key, dirname, RowParser, sampling):
    for day, deltas, ut, o_dens in make_deltas(key, dirname, RowParser):
        # 1. Split on chunks with gaps no longer than sampling;
        # 2. Iterate over datashifts 0 <= j < sampling;
        # 3. Look for sampling matches;
        # 4. Exclude multiples of matched samplings;
        # 5. Store (t_start, t_end, sampling) taking in acount sampling shift j;

        logger.info('[{}]\t {}: Total length of ut'.format(day, len(ut)))
        min_sequence_duration = 250 * sqrt(sampling)
        working_samplings = []
        logger.info('[{}]\t {}: sampling to check'.format(day, sampling))
        starts_at = 0
        continuous = True
        for idx in range(len(deltas)):
            continuous = continuous and o_dens[idx] is not None and not isnan(o_dens[idx]) and o_dens[idx] != 0

            if not continuous:
                starts_at = idx + 1
                continuous = True
                continue

            if deltas[idx] - sampling >= 0.5:
                year = date.fromtimestamp(ut[starts_at]).strftime('%Y / %j')
                if deltas[idx] > 500.:
                    logger.info(
                        chalk.red('{:0>4d}\t..\t\t\t{:.2f}'.format(sampling, deltas[idx]), bold=True, underline=True))
                segment_length = ut[idx] - ut[starts_at]

                if segment_length > min_sequence_duration:
                    logger.info(
                        chalk.green('{:0>4d}\t++[{}]\t{}\t\t{:.2f} > {}'.format(
                            sampling,
                            len(working_samplings),
                            year,
                            segment_length,
                            min_sequence_duration
                        ), bold=True, underline=True)
                    )
                    shift = 0
                    sub_working = []
                    while sum(deltas[starts_at:starts_at + shift]) < segment_length - min_sequence_duration:
                        points = verify_sampling(deltas[starts_at + shift:idx], sampling)
                        if points is not None and points > 0:
                            sub_working.append({
                                'indexes': (starts_at + shift, idx),
                                'length': idx - starts_at - shift + 1,
                                'points': points,
                                'segment': (ut[starts_at + shift], ut[idx]),
                                'duration': ut[idx] - ut[starts_at + shift],
                                'resolution': float(sampling) / points,
                                'day': day,
                            })
                            if (ut[idx] - ut[starts_at + shift]) > 0.9 * segment_length:
                                break
                        shift += 1

                    if len(sub_working) > 0:
                        working_samplings.append(sorted(sub_working, key=lambda x: x['duration'])[0])
                starts_at = idx + 1

        by_ut, by_length = artifacts(day, key, sampling)

        with open(by_ut, 'w') as artifact:
            json.dump(working_samplings, artifact)

        with open(by_length, 'w') as artifact:
            json.dump(sorted(
                working_samplings,
                key=lambda x: (-x['duration'], x['segment'][0])
            ), artifact)


def chunkup_samplings(key, dirname, RowParser):
    logger.info('{} at {}'.format(key, dirname))
    for sampling in [1]:  # range(1, 199):
        logger.info('{} -- sampling'.format(sampling))
        # by_ut, by_length = artifacts(key, sampling)
        # if not exists(by_ut) or not exists(by_length):
        sample(key, dirname, RowParser, sampling)


def main():
    chunkup_samplings('nacs', DE2SOURCE_NACS_DIR, SourceNACSRow)
    # chunkup_samplings('wats', DE2SOURCE_WATS_DIR, SourceWATSRow)


if __name__ == '__main__':
    main()
