from hashlib import sha256
from commands.utils.local_cache import LocalCache

from .types import FileList
from .monotone_files import monotone_files


@LocalCache
def deduplicated_files(source_marker: str) -> FileList:
    monotone_files_list = monotone_files(source_marker)

    hashes = {}
    for filename in monotone_files_list:
        fhash = sha256(open(filename, 'r').read().encode('utf-8').strip()).hexdigest()
        if fhash not in hashes:
            hashes[fhash] = []
        hashes[fhash].append(filename)

    return [ec[0] for ec in hashes.values()]
