from typing import List
from commands.utils.local_cache import LocalCache
from commands.parsers.file_parser import FileParserWindow

from numpy import nan, array, isnan, split, where, concatenate


def moving_average_sequence(x: array, window_len: int = 11, split_by_nans: bool = False) -> array:
    if len(x) == 0:
        return array([])

    window_len = int(window_len)
    if window_len % 2 == 0:
        window_len += 1

    if split_by_nans:
        chunks = split(x, where(isnan(x))[0])
        result = []
        for n, chunk in enumerate(chunks):
            if n != 0:
                result.append(array([nan]))
            result.append(moving_average(chunk[1:] if n != 0 else chunk, window_len=window_len, split_by_nans=False))
        return concatenate(result)

    result = []
    w2 = window_len // 2
    data_len = len(x)
    for i in range(data_len):
        base = min(i, w2, data_len - i - 1)
        sub_seq = x[i - base:i + base + 1]
        sub_seq = sub_seq[~isnan(sub_seq)]
        result.append(sum(sub_seq) / len(sub_seq) if len(sub_seq) != 0 else nan)
    return array(result)


@LocalCache()
def moving_average(data_chunk: FileParserWindow, *params_list: List[str], window_size: int=11) -> array:
    return array([moving_average_sequence(x, window_size, split_by_nans=False) for x in data_chunk.get(*params_list, transposed=True)])
