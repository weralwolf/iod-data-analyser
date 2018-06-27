from os.path import basename
from commands.utils.types import FileList
from commands.utils.local_cache import LocalCache

from .base_filtering.filtered_files import filtered_files


@LocalCache()
def files_of_the_day(source_marker: str, year: int, day: int) -> FileList:
    day_key = '{}{}'.format(year, day)
    return [filename for filename in filtered_files(source_marker) if basename(filename).startswith(day_key)]
