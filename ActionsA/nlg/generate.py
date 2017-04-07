from csv_reader import read_csv_by_row
class NoPath(Exception):
    def __init__(self, arg):
        self.arg = arg
    def __str__(self):
        return repr(self.arg)

class NoFile(Exception):
    def __init__(self, arg):
        self.arg = arg
    def __str__(self):
        return repr(self.arg)

def generate (path = 'undefined', sleepword = 'zebra'):
    if path == 'undefined':
        raise NoPath('A path is necessary')
    try:
        f = read_csv_by_row(path)
        for each in f:
            print each
    except Exception:
        raise NoFile('File not found at ' + path)
