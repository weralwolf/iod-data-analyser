from typing import Any, Dict, List, Optional
from logging import getLogger
from os.path import basename
from collections import OrderedDict
from commands.utils.cache_property import cached_property

from numpy import array

logger = getLogger('django')


class NoFileSpecifiedError(Exception):
    def __init__(self) -> None:
        super(NoFileSpecifiedError, self).__init__('Can not parse file, filename is not specified')


class RowParser(object):
    seed: List[OrderedDict] = [OrderedDict([])]
    drop_lines: int = 0
    filename: OrderedDict
    meta: Dict

    def __init__(self, filename: Optional[str] = None) -> None:
        logger.info('ROW PARSER FOR: {}'.format(filename))
        self.meta = dict(zip(
            self.filename.keys(),
            self._parse([self.filename], basename(filename)))
        ) if hasattr(self, 'filename') and filename is not None else dict()

    def parse(self, *lines: str) -> array:
        return self._parse(self.seed, *lines)

    def _parse(self, seed: List[OrderedDict], *lines: str) -> array:
        data = []
        delayed = {}
        for idx in range(len(seed)):
            for name, (computer, value_type) in seed[idx].items():
                if isinstance(computer, tuple):
                    start, stop = computer
                    data.append(value_type(lines[idx][start:stop].strip()))
                else:
                    delayed[len(data)] = computer
                    data.append(None)

        computed = dict(zip(self.names, data))
        if len(delayed):
            for idx, computer in delayed.items():
                data[idx] = computer(**computed, **self.meta)
        return data

    def stringify(self, row: List[Any]) -> str:
        return str(self.format_line.format(*row))

    @cached_property(ttl=0)
    def format_line(self) -> str:
        lines: List[str] = []
        for idx in range(len(self.seed)):
            formats = []
            for computer, type_cast in self.seed[idx].values():
                if not isinstance(computer, tuple):
                    continue
                start, stop = computer
                extension = '.3f' if type_cast == float else '.0f'
                formats.append(str(stop - start) + extension)
            lines.append('{: ' + '}{: '.join(formats) + '}')
        return '\n'.join(lines) + '\n'

    @cached_property(ttl=0)
    def names(self) -> List[str]:
        return [n for n in sum([list(line.keys()) for line in self.seed], [])]

    @property
    def lines(self) -> int:
        return len(self.seed)
