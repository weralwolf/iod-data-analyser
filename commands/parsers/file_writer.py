class FileWriter:
    def __init__(self, RowParser, data):
        self.row = RowParser()
        self.data = data

    def reflect(self, fileobject):
        fileobject.write('\n' * self.row.drop_lines)
        fileobject.writelines([self.row.stringify(row) for row in self.data])
