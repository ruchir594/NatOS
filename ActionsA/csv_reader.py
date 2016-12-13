import csv

delim = ','

def read_csv_by_row(filename):
    file_su = csv.reader(open(filename,"r"),delimiter=delim)
    return file_su
