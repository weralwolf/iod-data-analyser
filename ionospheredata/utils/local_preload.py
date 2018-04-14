import pickle
import hashlib
from os.path import join, dirname, realpath

CACHE_DIR = join(dirname(realpath(__file__)), "..", "..", "_objects")


def local_preload(name, caller, *args, cache_dir=CACHE_DIR, force_reload=False, **kwargs):
    def calculate():
        # print("{} does not exist. Computing\t{} objects".format(idx, name))
        res = caller(*args, **kwargs)
        with open(filename, "wb") as datafile:
            # print("\tObjects computed and stored for {}".format(name))
            pickle.dump(res, datafile)
            return res

    idx = hashlib.md5(str(name).encode('utf-8')).hexdigest()
    filename = join(cache_dir, idx + ".pydata")
    if force_reload:
        return calculate()
    try:
        with open(filename, "rb") as datafile:
            # print("{} used to load {} objects".format(idx, name))
            res = pickle.load(datafile)
            return res
    except IOError:
        return calculate()
