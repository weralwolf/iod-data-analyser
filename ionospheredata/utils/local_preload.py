import pickle
import hashlib
from os.path import join

from ionospheredata.settings import CACHE_DIR


def local_preload(name, caller, *args, cache_dir=CACHE_DIR, force_reload=False, **kwargs):
    def calculate():
        # print('{} does not exist. Computing\t{} objects'.format(idx, name))
        res = caller(*args, **kwargs)
        with open(filename, 'wb') as datafile:
            # print('\tObjects computed and stored for {}'.format(name))
            pickle.dump(res, datafile)
            return res

    idx = hashlib.md5(str(name).encode('utf-8')).hexdigest()
    filename = join(cache_dir, idx + '.pydata')
    if force_reload or CACHE_DIR is None:
        return calculate()
    try:
        with open(filename, 'rb') as datafile:
            # print('{} used to load {} objects'.format(idx, name))
            res = pickle.load(datafile)
            return res
    except EOFError:
        local_preload(name, caller, *args, cache_dir=cache_dir, force_reload=True, **kwargs)
    except IOError:
        return calculate()
