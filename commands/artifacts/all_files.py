from os import listdir
from typing import List
from fnmatch import fnmatch
from os.path import join
from commands.utils.cache import LocalCache

FileList = List[str]


@LocalCache
def all_files(dirname: str) -> FileList:
    return sorted([
        join(dirname, file)
        for file in listdir(dirname)
        if fnmatch(file, '*.asc') or fnmatch(file, '*.ASC')
    ])
