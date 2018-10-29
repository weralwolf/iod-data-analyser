from typing import Any, List, Tuple, Callable
from commands.utils.logger import logger
from commands.utils.local_cache import LocalCache
from commands.parsers.file_parser import FileParser, FileParserWindow
from commands.artifacts.parsed_data import parsed_data
from commands.artifacts.files_of_the_day import files_of_the_day

from numpy import array, isnan, round, concatenate


def adjust_sampling(deltas: List[int], sampling: int) -> Tuple[int, array]:
    sequence_filter_seed = [0]
    end_of_sequence = 0
    accumulated = 0
    for idx, delta in enumerate(deltas):
        accumulated += delta
        end_of_sequence += 1
        if accumulated < sampling:
            continue

        if accumulated > sampling:
            break

        sequence_filter_seed.append(idx + 1)
        accumulated = 0
    return end_of_sequence - 1, array(sequence_filter_seed)


def make_deltas(ut: array) -> array:
    """
    Counting deltas in UT. Example:
    [1, 2, 3, 5, 8] -> [1, 2, 3, 5, 8, 0] - [0, 1, 2, 3, 5, 8] = [1, 1, 1, 2, 3, -8] -> [1, 1, 2, 3]
    """
    empty_bin = array([0])
    return round(concatenate([ut, empty_bin]) - concatenate([empty_bin, ut]))[1:-1].astype(int)


def make_continuity_filter(data: FileParser, continuity_params: Tuple[str, ...], zero_cond: bool=True) -> Callable:
    if len(continuity_params) == 0:
        return lambda idx: True

    def is_present(value: Any) -> bool:
        return value is not None and not isnan(value) and (not zero_cond or value != 0)

    continuity_data = data.get(*continuity_params)

    def check_value(idx: int) -> bool:
        return all([is_present(continuity_data[idx, param_idx]) for param_idx in range(len(continuity_params))])
    return check_value


def sample(data: FileParser, sampling: int, continuity_params: Tuple[str, ...]) -> List[FileParserWindow]:
    """
    Sample data within fixed sampling supporting continuity of list of parameters.
    """
    local_ut = data.get('ut', transposed=True)[0] / 1000.
    deltas = make_deltas(local_ut)
    starts_at = 0
    is_continuous = make_continuity_filter(data, continuity_params)
    continuous = True
    sequences = []
    for idx, delta in enumerate(deltas):
        continuous = continuous and is_continuous(idx)
        if not continuous or delta > sampling or idx == len(deltas) - 1:
            # Segment is complete
            if starts_at == idx or starts_at + 1 == idx:  # Single or two isolated points
                continuous = True
                starts_at = idx + 1  # Since we will start from second element
                continue

            logger.error('{}:{} - our chunk'.format(starts_at, idx))
            max_sequence = (starts_at, starts_at, array([starts_at]))
            for shift in range(starts_at, idx - 1):
                local_start = starts_at + shift
                end_of_sequence, sub_sequence_filter = adjust_sampling(deltas[local_start:idx], sampling)
                if end_of_sequence == local_start:
                    continue

                if end_of_sequence - local_start > max_sequence[0] - max_sequence[1]:
                    max_sequence = (local_start, end_of_sequence + local_start, sub_sequence_filter + local_start)

                if local_ut[max_sequence[1]] - local_ut[max_sequence[0]] > local_ut[idx + 1] - local_ut[max_sequence[1]]:
                    break  # we apparently found maximum fit
            logger.error(max_sequence)
            if max_sequence[0] != max_sequence[1]:  # if we didn't stuck on the beginning
                sequences.append(max_sequence)

            logger.error('\t{}:{} - good'.format(max_sequence[0], max_sequence[1]))

            continuous = True
            starts_at = idx + 1
    logger.error(sequences)
    return [FileParserWindow(data, sequence_filter) for start, end, sequence_filter in sequences]


@LocalCache()
def sampled_day(source_marker: str, year: int, day: int, sampling: int, *continuity_params: str) -> List[FileParserWindow]:
    """
    Computes continuous data chunks inside of one day.
    :param source_marker: identificator of a data source.
    :param year: integer value representing year.
    :param day: integer value representing day.
    :param sampling: a sampling in seconds which is used to count continuity in UT.
    :param continuity_params: list of params continuity of which must be preserved.
    :return list of sampled data chunks.
    """
    if continuity_params is None:
        continuity_params = []
    files_list = files_of_the_day(source_marker, year, day)
    sampled_chunks: List[FileParserWindow] = []
    for file in sorted(files_list):
        logger.error(file)
        data = parsed_data(source_marker, file)
        sampled_chunks = [*sampled_chunks, *sample(data, sampling, continuity_params)]
    return sampled_chunks
