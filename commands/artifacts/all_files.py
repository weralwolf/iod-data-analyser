from os import listdir
from os.path import join
from commands.utils.types import FileList
from commands.utils.local_cache import LocalCache
from commands.utils.resolve_data_source import resolve_data_source


@LocalCache()
def all_files(source_marker: str) -> FileList:
    """
    List all (good and bad) files related to a data source.
    :param source_marker: identificator of a data source.
    :return list of all files in data source.
    """
    path, parser_class, selector, features_extractor = resolve_data_source(source_marker)
    return [
        join(path, file)
        for file in listdir(path)
        if selector(file)
    ]
