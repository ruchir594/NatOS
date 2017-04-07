import csv

delim = ','

def read_csv_by_row(filename):
    with open(filename, 'rb') as csvfile:
        file_su = csv.reader(csvfile, delimiter=delim)
        return file_su
    file_su = csv.reader(open(filename,"rb"),delimiter=delim)
    return file_su
