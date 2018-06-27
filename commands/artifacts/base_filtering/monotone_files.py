from commands.utils.types import FileList
from commands.utils.local_cache import LocalCache
from commands.artifacts.all_files import all_files

from .not_monotone_files import not_monotone_files


@LocalCache()
def monotone_files(source_marker: str) -> FileList:
    all_files_list = all_files(source_marker)
    not_monotone_files_list = not_monotone_files(source_marker)
    already_monotone = set(all_files_list).difference(set(not_monotone_files_list))

    # Here do fixes on `not_monotone_files_list` files if needed

    return already_monotone
