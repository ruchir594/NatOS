import csv

delim = ','

def read_csv_by_row(filename):
    with open(filename, 'rb') as csvfile:
        file_su = csv.reader(csvfile)
        return file_su
