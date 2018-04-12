from collections import OrderedDict
from ionospheredata.utils import cached_property
from os.path import basename


class RowParser(object):
    seed = [OrderedDict([])]
    drop_lines = 0

    def __init__(self, filename):
        self.meta = dict(zip(self.filename.keys(), self._parse([self.filename], basename(filename)))) if hasattr(self, 'filename') else dict()

    def parse(self, *lines):
        return self._parse(self.seed, *lines)

    def _parse(self, seed, *lines):
        data = []
        delayed = {}
        for idx in range(len(seed)):
            for computer in seed[idx].values():
                if isinstance(computer, tuple):
                    start, stop = computer
                    data.append(float(lines[idx][start:stop].strip()))
                else:
                    delayed[len(data)] = computer
                    data.append(None)

        computed = dict(zip(self.names, data))
        if len(delayed):
            for idx, computer in delayed.items():
                data[idx] = computer(**computed, **self.meta)
        return data

    @cached_property(ttl=0)
    def names(self):
        return sum([list(line.keys()) for line in self.seed], [])

    @property
    def lines(self):
        return len(self.seed)

