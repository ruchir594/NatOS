from csv_reader import read_csv_by_row
import csv

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
        with open(path, 'rb') as csvfile:
            file_su = csv.reader(csvfile)
            for each in file_su:
                print each
    except Exception:
        raise NoFile('File not found at ' + path)
