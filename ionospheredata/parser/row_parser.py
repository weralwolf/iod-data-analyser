from os.path import basename
from collections import OrderedDict

from ionospheredata.utils import cached_property


class NoFileSpecifiedError(Exception):
    def __init__(self):
        super(NoFileSpecifiedError, self).__init__('Can not parse file, filename is not specified')


class RowParser(object):
    seed = [OrderedDict([])]
    drop_lines = 0

    def __init__(self, filename=None):
        self.meta = dict(zip(
            self.filename.keys(),
            self._parse([self.filename], basename(filename)))
        ) if hasattr(self, 'filename') and filename is not None else dict()

    def parse(self, *lines):
        return self._parse(self.seed, *lines)

    def _parse(self, seed, *lines):
        data = []
        delayed = {}
        for idx in range(len(seed)):
            for computer, value_type in seed[idx].values():
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

    def stringify(self, row):
        return self.format_line.format(*row)

    @cached_property(ttl=0)
    def format_line(self):
        lines = []
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
    def names(self):
        return sum([list(line.keys()) for line in self.seed], [])

    @property
    def lines(self):
        return len(self.seed)
