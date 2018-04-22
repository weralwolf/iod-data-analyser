from math import ceil, floor
from os.path import join

from iod.a000_config import DE2_NACS_DIR, ARTEFACTS_DIR
from ionospheredata.utils import local_preload
from ionospheredata.parser import NACSRow, FileParser


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
        print("{}.\t{}\t- {}\t{} / {}".format(n, start, end, sampling, length))

    return chunks


def sample():
    datafiles = [join(DE2_NACS_DIR, fname.strip()) for fname in open(join(ARTEFACTS_DIR, 'NACS.good.txt'), 'r').readlines()]
    data = [
        local_preload(fname, FileParser, NACSRow, fname)
        for fname in sorted(datafiles)[:12]
    ]
    deltas = []
    distribution = {}

    ut = data[3].get('ut', transposed=True)[0]
    ongoing_sampling = round(ut[1] - ut[0])  # We're sure there's no files with less than 2 datapoints
    starts_at = 0
    for idx in range(1, len(ut)):
        sampling = round(ut[idx] - ut[idx - 1])
        deltas.append(sampling)
        if sampling != ongoing_sampling:
            sampling_len = idx - starts_at
            if distribution.get(sampling, 0) < sampling_len:
                distribution[sampling] = sampling_len

    # Ideal sampling can consist only as sum of present pieces. To widen a search,
    # I'll try to constitute samplings as different variations of a sums of smaller
    # samplings, where maximum appearences in the sum is the maximum of consequent
    # evenly sampled pieces and total sum does not overflow 500km / [8.6 km/s]
    # approx 58s.
    sampling_boundaries = (2, round(500 / 8.6))  # No gap longer than 500km
    matched_samiplings = []
    for sampling in range(*sampling_boundaries):
        repetition = False
        for match in matched_samiplings:
            if sampling % match == 0:
                repetition = True
                break
        if repetition:
            continue
        print("{}: sampling".format(sampling))
        match = 0
        for idx in range(0, len(deltas)):
            if match == sampling:
                match = 0
            elif match > sampling:
                break
            match += deltas[idx]
        else:
            matched_samiplings.append(sampling)
            print("\tMatches!")


def main():
    sample()


if __name__ == '__main__':
    main()
