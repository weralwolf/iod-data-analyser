from commands.filters.monotone import monotone
from commands.utils.local_cache import LocalCache

from .types import FileList
from .all_files import all_files


@LocalCache()
def not_monotone_files(source_marker: str) -> FileList:
    return [
        filename
        for filename in all_files(source_marker)
        if not monotone('ut', filename, source_marker)
    ]
