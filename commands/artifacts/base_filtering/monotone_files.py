from commands.utils.types import FileList
from commands.utils.local_cache import LocalCache
from commands.artifacts.all_files import all_files

from .not_monotone_files import not_monotone_files


@LocalCache()
def monotone_files(source_marker: str) -> FileList:
    """
    List monotone files related to a data source. File counted as monotone if UT parameter is monotone (nicely growing).
    :param source_marker: identificator of a data source.
    :return list of not monotone files.
    """
    all_files_list = all_files(source_marker)
    not_monotone_files_list = not_monotone_files(source_marker)
    already_monotone = set(all_files_list).difference(set(not_monotone_files_list))

    # Here do fixes on `not_monotone_files_list` files if needed

    return list(already_monotone)
