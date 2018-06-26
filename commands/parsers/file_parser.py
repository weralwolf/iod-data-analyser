from numpy import array, transpose, concatenate


def slice_by(it, n):
    return zip(*[it[i::n] for i in range(n)])


class FileParser:
    def __init__(self, RowParser, filename):
        self.row = RowParser(filename)
        self.names = list(self.row.names)
        self.filename = filename
        self._data = None
        self._parse()
        self._RowParser = RowParser

    def _parse(self):
        with open(self.filename, 'r') as datafile:
            lines = datafile.readlines()[self.row.drop_lines:]
            self._data = array([self.row.parse(*line) for line in slice_by(lines, self.row.lines)])

    def get(self, *params, transposed=False):
        idxs = [self.names.index(param) for param in params]
        if len(idxs) == 1:
            idx = idxs[0]
            data = self._data[:, idx:(idx + 1)]
        else:
            data = concatenate([self._data[:, idx:(idx + 1)] for idx in idxs], axis=1)

        return data if not transposed else transpose(data)

    @property
    def data(self):
        return self._data
