from os import stat, makedirs
from stat import S_ISDIR, ST_MODE
from os.path import exists


class ConfigurationError(Exception):
    pass


def isDir(dirname):
    return exists(dirname) or S_ISDIR(stat(dirname)[ST_MODE])


def assertConfig(statement, message='Configuration error'):
    if not statement:
        raise ConfigurationError(message)


def ensureDir(dirname):
    return makedirs(dirname, exist_ok=True)
