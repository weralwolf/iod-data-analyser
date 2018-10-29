from commands.utils.types import FileList
from commands.filters.monotone import monotone
from commands.utils.local_cache import LocalCache
from commands.artifacts.all_files import all_files


@LocalCache()
def not_monotone_files(source_marker: str) -> FileList:
    """
    List not monotone files related to a data source. File counted as not monotone if UT parameter is not monotone.
    :param source_marker: identificator of a data source.
    :return list of not monotone files.
    """
    return [
        filename
        for filename in all_files(source_marker)
        if not monotone('ut', filename, source_marker)
    ]
