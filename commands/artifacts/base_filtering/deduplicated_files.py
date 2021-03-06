from typing import Dict, List
from hashlib import sha256
from commands.utils.types import FileList
from commands.utils.local_cache import LocalCache

from .monotone_files import monotone_files


@LocalCache()
def deduplicated_files(source_marker: str) -> FileList:
    """
    List all monotone files without data duplicates, which are files which differe only by filenames.
    :param source_marker: identificator of a data source.
    :return list of unique files.
    """
    monotone_files_list = monotone_files(source_marker)

    hashes: Dict[str, List[str]] = {}
    for filename in monotone_files_list:
        fhash = sha256(open(filename, 'r').read().encode('utf-8').strip()).hexdigest()
        if fhash not in hashes:
            hashes[fhash] = []
        hashes[fhash].append(filename)

    return [list(sorted(ec))[0] for ec in hashes.values()]
