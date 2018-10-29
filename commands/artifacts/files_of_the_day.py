from os.path import basename
from commands.utils.types import FileList
from commands.utils.local_cache import LocalCache

from .base_filtering.filtered_files import filtered_files


@LocalCache()
def files_of_the_day(source_marker: str, year: int, day: int) -> FileList:
    """
    List files with data belonging to a particular day.
    :param source_marker: identificator of a data source.
    :return list of files with data of selected day.
    """
    day_key = '{}{:0>3}'.format(year, day)
    return [filename for filename in filtered_files(source_marker) if basename(filename).startswith(day_key)]
