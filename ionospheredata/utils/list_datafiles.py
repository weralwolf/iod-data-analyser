from os.path import join
from os import listdir
from fnmatch import fnmatch


def list_datafiles(dirname):
    return sorted([join(dirname, file) for file in listdir(dirname) if fnmatch(file, "*.asc") or fnmatch(file, "*.ASC")])



