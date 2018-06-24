from commands.filters.monotone import monotone
from commands.utils.local_cache import LocalCache
from commands.utils.resolve_data_source import resolve_data_source

from .types import FileList
from .all_files import all_files


@LocalCache
def not_monotone_files(source_marker: str) -> FileList:
    path, parser_class, selector, features_extractor = resolve_data_source(source_marker)
    return [
        filename
        for idx, filename in all_files(source_marker)
        if not monotone('ut', filename, parser_class)
    ]
