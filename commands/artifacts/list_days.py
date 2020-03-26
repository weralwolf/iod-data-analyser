from typing import List, Tuple
from commands.utils.local_cache import LocalCache
from commands.artifacts.all_files import all_files
from commands.utils.resolve_data_source import resolve_data_source
from commands.artifacts.base_filtering.filtered_files import filtered_files


@LocalCache()
def list_days(source_marker: str, filtered: bool = False) -> List[Tuple[int, int]]:
    """
    List all days available for a data source.
    :param source_marker: identificator of a data source.
    :return list of tuples, where first element is a year and second is a day.
    """
    files_list = all_files(source_marker) if not filtered else filtered_files(source_marker)
    path, parser_class, selector, features_extractor = resolve_data_source(source_marker)
    days_set = set()
    for file in files_list:
        features = features_extractor(file)
        days_set.add((int(features['year'], 10), int(features['day'], 10)))

    return list(days_set)
