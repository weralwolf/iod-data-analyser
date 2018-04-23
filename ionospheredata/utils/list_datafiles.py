from os import listdir
from fnmatch import fnmatch
from os.path import join


def list_datafiles(dirname):
    return sorted([join(dirname, file) for file in listdir(dirname) if fnmatch(file, '*.asc') or fnmatch(file, '*.ASC')])
