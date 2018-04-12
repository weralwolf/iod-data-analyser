from iod.a000_config import DE2_NACS_DIR, DE2_WATS_DIR
from ionospheredata.parser import FileParser, NACSRow, WATSRow

import pickle, hashlib
from os.path import join, dirname, realpath, basename
from fnmatch import fnmatch
from os import listdir


CACHE_DIR = join(dirname(realpath(__file__)), "_objects")
FORCE_RELOAD_CACHE = False

def local_preload(name, caller, *args, **kwargs):
    def calculate():
        # print("{} does not exist. Computing\t{} objects".format(idx, name))
        res = caller(*args, **kwargs)
        with open(filename, "wb") as datafile:
            # print("\tObjects computed and stored for {}".format(name))
            pickle.dump(res, datafile)
            return res

    idx = hashlib.md5(str(name).encode('utf-8')).hexdigest()
    filename = join(CACHE_DIR, idx + ".pydata")
    if FORCE_RELOAD_CACHE:
        return calculate()
    try:
        with open(filename, "rb") as datafile:
            # print("{} used to load {} objects".format(idx, name))
            res = pickle.load(datafile)
            return res
    except IOError:
        return calculate()


def list_datafiles(dirname):
    return sorted([join(dirname, file) for file in listdir(dirname) if fnmatch(file, "*.asc") or fnmatch(file, "*.ASC")])


def check_ut_monotone(filename, RowParser):
    filedata = local_preload(filename, FileParser, RowParser, filename)
    uts = filedata.get('ut_of_day', transposed=True)[0]
    for idx in range(1, len(uts)):
        if uts[idx] <= uts[idx - 1]:
            return False
    return True


def bad_files(RowParser, dirname):
    bads = []
    datafiles = list_datafiles(dirname)
    for idx, filename in enumerate(datafiles):
        if not check_ut_monotone(filename, RowParser):
            # print("{} BAD ... {}".format(idx, filename))
            bads.append(filename)
    return bads


if __name__ == '__main__':
    bad_nacs_files = local_preload('nacs_bad_files', bad_files, NACSRow, DE2_NACS_DIR)
    bad_subclass = set()
    for n, badfile in enumerate(bad_nacs_files):
        # print("{}. {}".format(n, basename(badfile)))
        filedata = local_preload(badfile, FileParser, NACSRow, badfile)
        uts = filedata.get('ut_of_day', transposed=True)[0]
        for idx in range(1, len(uts)):
            if uts[idx] == uts[idx - 1]:  # Must be <=
                bad_subclass.add(badfile)
                print("\t{}[{}/{}] {} {} {}".format('!' if idx + 1 != len(uts) else ' ', idx + 1, len(uts), uts[idx - 1], '=' if uts[idx] == uts[idx - 1] else '>', uts[idx]))
    print("Bad subclass. Equality: {}".format(len(bad_subclass)))

