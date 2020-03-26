from typing import Any, List, Tuple, Callable, Optional
from os.path import basename
from commands.utils.logger import logger  # noqa: F401

from numpy import array, transpose, concatenate

from .row_parser import RowParser


def slice_by(it: List[str], n: int) -> List[Tuple[Any, ...]]:
    return [j for j in zip(*[it[i::n] for i in range(n)])]


class FileParser:
    row: RowParser
    names: List[str]
    filename: str
    _data: Optional[array]

    def __init__(self, RowParser: Callable, filename: str, shallow: bool = False) -> None:
        self.row = RowParser(filename)
        self.names = list(self.row.names)
        self.filename = filename
        self._data = None
        self.RowParser = RowParser

        if not shallow:
            self._parse()

    def _parse(self) -> None:
        with open(self.filename, 'r') as datafile:
            lines = datafile.readlines()[self.row.drop_lines:]
            self._data = array([self.row.parse(*line) for line in slice_by(lines, self.row.lines)])

    def get(self, *params: Any, transposed: bool = False) -> array:
        idxs = [self.names.index(param) for param in params]
        if len(idxs) == 1:
            idx = idxs[0]
            data = self.data[:, idx:(idx + 1)]
        else:
            data = concatenate([self.data[:, idx:(idx + 1)] for idx in idxs], axis=1)

        return data if not transposed else transpose(data)

    @property
    def data(self) -> array:
        return array([]) if self._data is None else self._data

    def __repr__(self) -> str:
        return '<{} of {} [{:.2f} - {:.2f}]>'.format(
                self.__class__.__name__,
                basename(self.filename),
                self.data[0, 0] / 1000.,
                self.data[-1, 0] / 1000.
        )


class FileParserWindow(FileParser):
    def __init__(self, origin: FileParser, sequence_filter: array) -> None:
        super().__init__(origin.RowParser, origin.filename, shallow=True)
        if origin._data is not None:
            self._data = origin.data[sequence_filter, :]
        self.cache_hash = origin.filename + ','.join(map(str, sequence_filter))
