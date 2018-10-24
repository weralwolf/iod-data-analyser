from typing import List, Tuple
from commands.utils.local_cache import LocalCache
from commands.artifacts.all_files import all_files
from commands.utils.resolve_data_source import resolve_data_source


@LocalCache()
def list_days(source_marker: str) -> List[Tuple[int, int]]:
    files_list = all_files(source_marker)
    path, parser_class, selector, features_extractor = resolve_data_source(source_marker)
    days_set = set()
    for file in files_list:
        features = features_extractor(file)
        days_set.add((int(features['year']), int(features['day'], 10)))

    return list(days_set)
