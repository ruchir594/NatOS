import json
import time

from reader import get_columns, convert_type

json_template_file = 'template.json'
json_db_file = 'data.json'

def init_json(file, db_name):
    data = {"db_name": db_name, "rows":[]}
    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def get_element(file, id):
    '''
        The purpose of this function is to either make a new element with primary key 'id'
        Or return an existing element with primary key 'id'
        The user can have his own keys like 'unique key' in the template
    '''
    with open(file, 'r') as f:
         data = json.load(f)
    flag = False
    for i in data["rows"]:
        if i["id"] == id:
            flag = True
            with open(file, 'w') as f:
                 json.dump(data, f)
            return i
    flag = False
    if flag == False:
        column_names, column_types = get_columns(json_template_file)
        # JSON object
        json_string_element = '{"id":"'+id+'",'
        #the id is added in quotes, becasue ID can be a number, or a bunch of characters. Doesn't matter
        #this ID is used to either retrieve an element. or make a new element.
        i=0
        for i in range(len(column_names)):
            json_string_element = json_string_element + '"' + column_names[i] + '": ' + convert_type(column_types[i]) + ','
        json_string_element = json_string_element[:-1] #to remove the last extra ','
        json_string_element = json_string_element + '}'
        # Now we have a fully initialized JSON string
        killbill = json.loads(json_string_element)
        data["rows"].append(killbill)
        with open(file, 'w') as f:
             json.dump(data, f)
        return killbill

def update_element(file, element):
    '''
    This function updates thr row. by the unique element ['id']
    '''
    with open(file, 'r') as f:
         data = json.load(f)
    column_names, column_types = get_columns(json_template_file)
    for i in data['rows']:
        if i['id'] == element['id']:
            for each_name in column_names:
                i[each_name] = element[each_name]
            break
    with open(file, 'w') as f:
         json.dump(data, f)

def wash_element(file, element):
    with open(file, 'r') as f:
         data = json.load(f)
    column_names, column_types = get_columns(json_template_file)
    for i in data['rows']:
        if i['id'] == element['id']:
            for (each_name, each_type) in zip(column_names, column_types):
                i[each_name] = convert_type(each_type)
        break
    with open(file, 'w') as f:
         json.dump(data, f)

#print get_element('data.json','103')
