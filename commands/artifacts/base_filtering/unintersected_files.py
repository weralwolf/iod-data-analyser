from typing import Any, List
from os.path import basename
from commands.utils.types import FileList
from commands.utils.local_cache import LocalCache
from commands.artifacts.parsed_data import parsed_data
from commands.utils.resolve_data_source import resolve_data_source

from .deduplicated_files import deduplicated_files


@LocalCache()
def unintersected_files(source_marker: str) -> FileList:
    """
    List files which does not intersect in UT.
    :param source_marker: identificator of a data source.
    :return list of files not intersecting in UT.
    """
    deduplicated_files_list = deduplicated_files(source_marker)
    path, parser_class, selector, features_extractor = resolve_data_source(source_marker)

    unitersected: List[Any] = []
    previous_key = None
    for filename in sorted(deduplicated_files_list):
        data = parsed_data(source_marker, filename)
        features = features_extractor(basename(filename))
        key = '{year}.{day}'.format(**features)
        ut = data.get('ut', transposed=True)[0]

        if key != previous_key or len(unitersected) == 0:
            previous_key = key
            unitersected.append((filename, ut[0], ut[-1]))
            continue

        if ut[0] <= unitersected[-1][1] <= ut[-1] or ut[0] <= unitersected[-1][2] <= ut[-1]:
            unitersected.pop()
        else:
            unitersected.append((filename, ut[0], ut[-1]))

    return [filename for filename, start, end in unitersected]
