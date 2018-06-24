from commands.utils.cache import LocalCache
from commands.filters.monotone import monotone

from .all_files import all_files


@LocalCache
def monotone_files(RowParser, dirname):
    return [
        filename
        for idx, filename in all_files(dirname)
        if monotone('ut', filename, RowParser)
    ]
