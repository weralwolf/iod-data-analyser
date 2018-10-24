from typing import Any, Callable

from numpy import array


class FileWriter:
    def __init__(self, row_parser: Callable, data: array) -> None:
        self.row = row_parser()
        self.data = data

    def reflect(self, fileobject: Any) -> None:
        fileobject.write('\n' * self.row.drop_lines)
        fileobject.writelines([self.row.stringify(row) for row in self.data])
