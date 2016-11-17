import sys
sys.path.insert(0, './')
sys.path.insert(0, './jsondb')
import reader, manage_element
import csv_reader

def get_tf(element):
    column_names, column_types = reader.get_columns(json_template_file = 'template.json')
    param_array = []
    for (each_name, each_type) in zip(column_names, column_types):
        if element[each_name] == reader.check_type(each_type):
            param_array.append('0')
        else:
            param_array.append('1')
    return param_array

def get_action_params_id(element):
    param_array = get_tf(element)
    rows = csv_reader.read_csv_by_row('action_params.csv')
    for each_row in rows:
        if each_row[1:] == param_array[1:]:
            return each_row[0]

#print get_action_params_id(manage_element.get_element('data.json','104'))
