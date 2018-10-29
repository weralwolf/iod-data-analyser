import pickle
import logging
from os import remove, listdir
from typing import Any, List, Callable, Optional
from fnmatch import fnmatch
from hashlib import md5
from os.path import join
from commands.settings.base import CACHE_DIR

logger = logging.getLogger(__file__)


class LocalCache:
    """
    Local filesystem cache for project to store heavy computations results.
    @TODO: Figure out how to cache execution of class functions.

    Usage:
    @LocalCache(hash_key)
    def func(...):
        ...
        return expected_value

    Hash for function will be computed by `hash_key` parameter and values of arguments.
    If argument object have `cache_hash` property it will be used.
    """
    cachefile_extension = 'pydata'

    def __init__(self, key: Optional[str]=None, force_reload: bool=False, cache_dir: str=CACHE_DIR) -> None:
        self.key = key
        self.force_reload = force_reload
        self.cache_dir = cache_dir

    def __call__(self, func: Callable) -> Callable:
        key = self.key if self.key is not None else func.__name__

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            task_hash = self._hash(key, *args, **kwargs)
            exists, result = self._recover_result(task_hash)
            if exists:
                logger.error('cache: {} / {}'.format(func.__name__, task_hash))
                return result
            logger.error('comp:  {} / {}'.format(func.__name__, task_hash))
            result = func(*args, **kwargs)
            return self._cache_result(task_hash, result)
        return wrapper

    def _hash(self, key: str, *args: Any, **kwargs: Any) -> str:
        params_str = self._process_parameters(*args, **kwargs)
        return md5(str(key + params_str).encode('utf-8')).hexdigest()

    def _filename(self, hash: str) -> str:
        return join(self.cache_dir, hash + '.' + self.cachefile_extension)

    def _cache_result(self, hash: str, result: Any) -> Any:
        with open(self._filename(hash), 'wb') as datafile:
            pickle.dump(result, datafile)
        return result

    def _recover_result(self, hash: str) -> Any:
        try:
            with open(self._filename(hash), 'rb') as datafile:
                return True, pickle.load(datafile)
        except EOFError:
            return False, None
        except IOError:
            return False, None

    def _process_parameters(self, *args: Any, **kwargs: Any) -> str:
        return ';'.join(
            [self._process_value(arg) for arg in args] +
            ['{}={}'.format(name, self._process_value(arg)) for name, arg in kwargs.items()]
        )

    def _process_value(self, value: Any) -> str:
        if hasattr(value, 'cache_hash'):
            return str(value.cache_hash)
        return repr(value)

    @classmethod
    def clear_cache(cls, cache_dir: str=CACHE_DIR) -> List[str]:
        removed_hashes = []
        for filename in listdir(cache_dir):
            if fnmatch(filename, '*.' + cls.cachefile_extension):
                remove(join(cache_dir, filename))
                removed_hashes.append(filename[:-(1 + len(cls.cachefile_extension))])
        return removed_hashes
