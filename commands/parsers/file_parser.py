from commands.utils.logger import logger  # noqa: F401

from numpy import array, transpose, concatenate


def slice_by(it, n):
    return zip(*[it[i::n] for i in range(n)])


class FileParser:
    def __init__(self, RowParser, filename, shallow=False):
        self.row = RowParser(filename)
        self.names = list(self.row.names)
        self.filename = filename
        self._data = None
        self.RowParser = RowParser

        if not shallow:
            self._parse()

    def _parse(self):
        with open(self.filename, 'r') as datafile:
            lines = datafile.readlines()[self.row.drop_lines:]
            self._data = array([self.row.parse(*line) for line in slice_by(lines, self.row.lines)])

    def get(self, *params, transposed=False):
        idxs = [self.names.index(param) for param in params]
        if len(idxs) == 1:
            idx = idxs[0]
            data = self.data[:, idx:(idx + 1)]
        else:
            data = concatenate([self.data[:, idx:(idx + 1)] for idx in idxs], axis=1)

        return data if not transposed else transpose(data)

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return '<{}[{:.2f} - {:.2f}]>'.format(self.__class__.__name__, self.data[0, 0] / 1000., self.data[-1, 0] / 1000.)


class FileParserWindow(FileParser):
        def __init__(self, origin: FileParser, sequence_filter: array):
            super().__init__(origin.RowParser, origin.filename, shallow=True)
            self._data = origin._data[sequence_filter, :]
