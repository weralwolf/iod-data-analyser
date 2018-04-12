from fnmatch import fnmatch
from os import listdir
from math import floor

from iod.a000_config import DE2_NACS_DIR
from iod.a000_config import DE2_WATS_DIR

from ionospheredata.parser import FileParser, NACSRow, WATSRow
from os.path import basename, join

from matplotlib import pyplot as plt
from matplotlib import collections


from os.path import join, realpath, dirname

import pickle, hashlib


CURRENT_DIR = join(dirname(realpath(__file__)), "_objects")
FORCE_RELOAD_CACHE = False

def local_preload(name, caller, *args, **kwargs):
    def calculate():
        print("{} does not exist. Computing\t{} objects".format(idx, name))
        res = caller(*args, **kwargs)
        with open(filename, "wb") as datafile:
            print("\tObjects computed and stored for {}".format(name))
            pickle.dump(res, datafile)
            return res

    idx = hashlib.md5(str(name).encode('utf-8')).hexdigest()
    filename = join(CURRENT_DIR, idx + ".pydata")
    if FORCE_RELOAD_CACHE:
        return calculate()
    try:
        with open(filename, "rb") as datafile:
            print("{} used to load {} objects".format(idx, name))
            res = pickle.load(datafile)
            return res
    except IOError:
        return calculate()

class FileSequence:
    def __init__(self, RowParser, filename):
        self.tag = basename(filename).lower().split('.')[0]
        self.parser = FileParser(RowParser, filename)
        self.ut = self.parser.get('ut', transposed=True)[0]


def parse(RowParser, dirname):
    files = {}
    datafiles = sorted([file for file in listdir(dirname) if fnmatch(file, "*.asc") or fnmatch(file, "*.ASC")])
    print("Datadir {} contains {} datafiles".format(dirname, len(datafiles)))
    for n, file in enumerate(datafiles):
        fs = local_preload(file, FileSequence, RowParser, join(dirname, file))
        files[fs.tag] = fs
        print("\t{}/{}\t{} has\t{}\ttimestamps".format(n + 1, len(datafiles), basename(file), len(fs.ut)))

    print("Totally: {}".format(len(files)))
    marks = sum([[(f.ut[0], f.tag, True), (f.ut[-1], f.tag, False)]  for f in files.values()], [])
    sorted(marks, key=lambda x: x[0], reverse=True)

    opened = set()
    patches = []
    for ut, tag, is_start in marks:
        if is_start:
            opened.add(tag)
        else:
            for otag in opened:
                if tag == otag:
                    continue
                patches.append((max(files[otag].ut[0], files[tag].ut[0]), ut, otag))
            opened.remove(tag)

    for n, patch in enumerate(patches):
        print("{}. {!r}".format(n, str(patch)))

    return files, patches

"""
Data integrity checks:
1. UT in NACS files can overleap on the next day (example: 1982040T233640_0_DE2_NACS_1S_V01.ASC);
2. After fixing UT shifts it seems that there's no overlaps;
3. On cross check of data sampling I detected negative values, hence problems are not gone;

There's 27 problematic points: (-82104, 1), (-29584, 1), (-7243, 1), (-6741, 1), (-6533, 1), (-5132, 1), (-3862, 1), (-3659, 1), (-3438, 1), (-2699, 1), (-2697, 1), (-2667, 1), (-2486, 1), (-2389, 1), (-2370, 1), (-2333, 1), (-2151, 1), (-1875, 1), (-1797, 1), (-1727, 1), (-1469, 1), (-1285, 1), (-1241, 1), (-1197, 1), (-857, 1), (-461, 1), (-173, 1)

From 1981249t113820_0_de2_nacs_1s_v01 to 1981249t113820_0_de2_nacs_1s_v01 sampling is -2696.967999994755
From 1981263t235500_0_de2_nacs_1s_v01 to 1981263t235500_0_de2_nacs_1s_v01 sampling is -172.99899995326996
From 1981264t073640_0_de2_nacs_1s_v01 to 1981264t073640_0_de2_nacs_1s_v01 sampling is -2150.003000020981
From 1981265t150820_0_de2_nacs_1s_v01 to 1981265t150820_0_de2_nacs_1s_v01 sampling is -3861.9919999837875
From 1981267t231820_0_de2_nacs_1s_v01 to 1981267t231820_0_de2_nacs_1s_v01 sampling is -2369.9789999723434
From 1981276t194640_0_de2_nacs_1s_v01 to 1981276t194640_0_de2_nacs_1s_v01 sampling is -7242.943000018597
From 1981285t163320_2_de2_nacs_1s_v01 to 1981285t163320_2_de2_nacs_1s_v01 sampling is -1240.0030000209808
From 1981296t140820_0_de2_nacs_1s_v01 to 1981296t140820_0_de2_nacs_1s_v01 sampling is -1796.0029999613762
From 1981306t124500_0_de2_nacs_1s_v01 to 1981306t124500_0_de2_nacs_1s_v01 sampling is -2332.9959999918938
From 1981316t164500_0_de2_nacs_1s_v01 to 1981316t164500_0_de2_nacs_1s_v01 sampling is -856.0039999485016
From 1981320t221500_0_de2_nacs_1s_v01 to 1981320t221500_0_de2_nacs_1s_v01 sampling is -5131.065999984741
From 1981320t224000_0_de2_nacs_1s_v01 to 1981320t224000_0_de2_nacs_1s_v01 sampling is -2698.035000026226
From 1981347t213140_0_de2_nacs_1s_v01 to 1981347t213140_0_de2_nacs_1s_v01 sampling is -82103.85099995136
From 1981348t222820_2_de2_nacs_1s_v01 to 1981348t222820_2_de2_nacs_1s_v01 sampling is -1874.989999949932
From 1981353t195140_0_de2_nacs_1s_v01 to 1981353t195140_0_de2_nacs_1s_v01 sampling is -6740.044999957085
From 1981364t061000_0_de2_nacs_1s_v01 to 1981364t061000_0_de2_nacs_1s_v01 sampling is -2388.0159999728203
From 1981364t221500_0_de2_nacs_1s_v01 to 1981364t221500_0_de2_nacs_1s_v01 sampling is -2485.9769999980927
From 1982007t080640_0_de2_nacs_1s_v01 to 1982007t080640_0_de2_nacs_1s_v01 sampling is -1196.9979999661446
From 1982021t084820_0_de2_nacs_1s_v01 to 1982021t084820_0_de2_nacs_1s_v01 sampling is -1284.0170000195503
From 1982030t191320_0_de2_nacs_1s_v01 to 1982030t191320_0_de2_nacs_1s_v01 sampling is -29583.95499998331
From 1982041t231640_0_de2_nacs_1s_v01 to 1982041t231640_0_de2_nacs_1s_v01 sampling is -6532.06400001049
From 1982148t225640_0_de2_nacs_1s_v01 to 1982148t225640_0_de2_nacs_1s_v01 sampling is -3658.979999959469
From 1982206t100500_0_de2_nacs_1s_v01 to 1982206t100500_0_de2_nacs_1s_v01 sampling is -1726.9700000286102
From 1982210t050820_0_de2_nacs_1s_v01 to 1982210t050820_0_de2_nacs_1s_v01 sampling is -2666.9420000314713
From 1982318t234320_0_de2_nacs_1s_v01 to 1982318t234320_0_de2_nacs_1s_v01 sampling is -1468.9890000224113
From 1982324t234320_0_de2_nacs_1s_v01 to 1982324t234320_0_de2_nacs_1s_v01 sampling is -460.9869999885559
From 1982329t050820_0_de2_nacs_1s_v01 to 1982329t050820_0_de2_nacs_1s_v01 sampling is -3437.0040000081062
"""

def ut_spectrum(files):
    uts = []
    N = len(files)
    for n, key in enumerate(sorted(files.keys())):
        print("{} / {}\t uts for {}".format(n + 1, N, key))
        uts += [(ut, key) for ut in files[key].parser.get('ut', transposed=True)[0]]
    return uts

def main():
    # local_preload("wats-source-data", parse, WATSRow, DE2_WATS_DIR)
    files, patches = local_preload("nacs-source-data", parse, NACSRow, DE2_NACS_DIR)
    # print("Drawing...")
    # ut = local_preload('nacs-ut-spectrum', ut_spectrum, files)
    # print("There's {} ut dots".format(len(ut)))
    # for idx in range(1, len(ut)):
    #     if ut[idx][0] - ut[idx - 1][0] < 0:
    #         print("{!r}: from {} to {} sampling is {}".format(ut[idx - 1][1] != ut[idx - 1][1], ut[idx - 1][1], ut[idx - 1][1], ut[idx][0] - ut[idx - 1][0]))
    #
    # # plt.plot(bins, hist, 'r')
    # # plt.grid(True)
    # # plt.show()
    # # for n, key in enumerate(list(sorted(files.keys()))[20:30]):
    # #     print("Data of {}".format(key))
    # #     fs = files[key]
    # #     if fs.ut[-1] - fs.ut[0] < 0:
    # #         print("{}.\t{}:\t{}\t... {}\t= {}\t: {}".format(n, key, fs.ut[0], fs.ut[-1], fs.ut[-1] - fs.ut[0], len(fs.ut)))
    # #     plt.plot(fs.parser.get('ut', transposed=True)[0], fs.parser.get('o_dens', transposed=True)[0], 'g' if n % 2 else 'r')
    # #     plt.show()


if __name__ == '__main__':
    main()

