from numpy import array
from numpy import concatenate
from numpy import transpose


def slice_by(it, n):
    return zip(*[it[i::n] for i in range(n)])

class FileParser:
    def __init__(self, RowParser, filename):
        self.row = RowParser(filename)
        self.names = list(self.row.names)
        self.filename = filename
        self._data = None
        self._parse()
        self._ut_jump_fix()

    def _parse(self):
        with open(self.filename, 'r') as datafile:
            lines = datafile.readlines()[self.row.drop_lines:]
            self._data = array([self.row.parse(*line) for line in slice_by(lines, self.row.lines)])

    def get(self, *params, transposed=False):
        idxs = [self.names.index(param) for param in params]
        data = None
        if len(idxs) == 1:
            idx = idxs[0]
            data = self._data[:, idx:(idx + 1)]
        else:
            data = concatenate((self._data[:, idx:(idx + 1)] for idx in idxs), axis=1)
        return data if not transposed else transpose(data)

    def _ut_jump_fix(self):
        utidx = self.names.index('ut')
        ut = self._data[:, utidx]
        diff = list(filter(lambda x: x[1] < 0, [(idx, ut[idx] - ut[idx - 1]) for idx in range(1, len(ut))]))
        if len(diff) == 0:
            return  # There's no jumps to fix
        if len(diff) > 1:
            raise ValueError("There's more than 1 jump in data at: {}".format(self.filename))
        print("Fixing ut jump in data of {}".format(self.filename))
        idx = diff[0][0]
        self._data[idx:, utidx] += 24 * 3600  # seconds in 1 day

    @property
    def data(self):
        return self._data
