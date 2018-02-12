from collections import OrderedDict


class RowParser:
    seed = [OrderedDict([])]
    drop_lines = 0

    def parse(self, *lines):
        return self._parse(self.seed, *lines)

    def _parse(self, seed, *lines):
        data = []
        for idx in range(self.lines):
            for start, stop in self.seed[idx].values():
                data.append(float(lines[idx][start:stop].strip()))
        return data

    @property
    def names(self):
        return sum([list(line.keys()) for line in self.seed], [])

    @property
    def lines(self):
        return len(self.seed)
