import json
from math import ceil, floor
from os.path import join, exists

from numpy import concatenate

from iod.a000_config import DE2_NACS_DIR, DE2_WATS_DIR, ARTEFACTS_DIR
from ionospheredata.utils import local_preload
from ionospheredata.parser import NACSRow, WATSRow, FileParser


def round(x):
    return ceil(x) if x - floor(x) > 0.5 else floor(x)


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
        print('{}.\t{}\t- {}\t{} / {}'.format(n, start, end, sampling, length))

    return chunks


def find_samipling(deltas, upper_sampling):
    matched_samiplings = []
    for sampling in range(2, upper_sampling + 1):
        repetition = False
        for match in matched_samiplings:
            if sampling % match == 0:
                repetition = True
                break
        if repetition:
            continue
        match = 0
        for idx in range(0, len(deltas)):
            if match == sampling:
                match = 0
            elif match > sampling:
                break
            match += deltas[idx]
        else:
            matched_samiplings.append(sampling)
            # print('\t{}: matched!'.format(sampling))
    return matched_samiplings


def artifacts(key, sampling):
    return (
        join(ARTEFACTS_DIR, '{}.{:0>4d}s.sampling.by_ut.json'.format(key.upper(), sampling)),
        join(ARTEFACTS_DIR, '{}.{:0>4d}s.sampling.by_length.json'.format(key.upper(), sampling))
    )


def make_deltas(key, dirname, RowParser):
    print('{}. Reading datafiles'.format(key.upper()))
    datafiles = [join(dirname, fname.strip()) for fname in open(join(ARTEFACTS_DIR, '{}.good.txt'.format(key.upper())), 'r').readlines()]
    data = [
        local_preload(fname, FileParser, RowParser, fname)
        for fname in sorted(datafiles)
    ]
    deltas = []
    print('{}. Concatenate total ut'.format(key.upper()))
    ut = concatenate([datafile.get('ut', transposed=True)[0] for datafile in data], axis=0)
    print('{}. Compute deltas'.format(key.upper()))
    for idx in range(1, len(ut)):
        deltas.append(ut[idx] - ut[idx - 1])

    return deltas, ut


def sample(key, dirname, RowParser, sampling):
    deltas, ut = local_preload('{}-deltas'.format(key), make_deltas, key, dirname, RowParser)

    # 1. Split on chunks with gaps no longer than sampling;
    # 2. Iterate over datashifts 0 <= j < sampling;
    # 3. Look for sampling matches;
    # 4. Exclude multiples of matched samplings;
    # 5. Store (t_start, t_end, sampling) taking in acount sampling shift j;

    print('{}: Total length of ut'.format(len(ut)))
    minimum_sequence_length = 500
    working_samplings = []
    print('{}: sampling to check'.format(sampling))
    starts_at = 0
    for idx in range(len(deltas)):
        if deltas[idx] > sampling and idx - starts_at > minimum_sequence_length:
            printed = False
            shift = 0
            while sum(deltas[starts_at:starts_at + shift]) < sampling:
                inner_samplings = find_samipling(deltas[starts_at + shift:idx], sampling)
                if len(inner_samplings) > 0:
                    if not printed:
                        print('\t{} - {}'.format(ut[starts_at], ut[idx]))
                        printed = True
                    print('\t\t+{} / {}: shift / samplings count'.format(shift, len(inner_samplings)))
                    working_samplings.append({
                        'indexes': (starts_at + shift, idx),
                        'segment': (ut[starts_at + shift], ut[idx]),
                        'lengt': idx - starts_at - shift + 1,
                        'duration': ut[idx] - ut[starts_at + shift],
                        'samplings': inner_samplings,
                    })
                shift += 1
            starts_at = idx + 1

    by_ut, by_length = artifacts(key, sampling)

    with open(by_ut, 'w') as artifact:
        json.dump(working_samplings, artifact)

    with open(by_length, 'w') as artifact:
        json.dump(sorted(
            working_samplings,
            key=lambda x: (-x['duration'], max(x['samplings']), x['segment'][0])
        ), artifact)


def chunkup_samplings(key, dirname, RowParser):
    for sampling in range(2, round(1700 / 8.6) + 1):  # No gap longer than 1700km
        by_ut, by_length = artifacts(key, sampling)
        if not exists(by_ut) or not exists(by_length):
            sample(key, dirname, RowParser, sampling)


def main():
    chunkup_samplings('nacs', DE2_NACS_DIR, NACSRow)
    chunkup_samplings('wats', DE2_WATS_DIR, WATSRow)


if __name__ == '__main__':
    main()
