import sys
sys.path.insert(0, './')
sys.path.insert(0, './jsondb')
sys.path.insert(0, './nle')
import reader, manage_element

json_db_file = 'data.json'
json_file_name = 'template.json'

#######              ID                    #######
# userid, messengerid, or uniqueid for each user #

id = 101 #generate someway

def does_match(json_object,column_names):
    for each in column_names:
        try:
            just = json_object[each]
        except Exception:
            print "JSON Object does not match " + json_file_name + " column_names! Sorry. "
            return None
    return True

def fill_element(element, ents):
    column_names, column_types = reader.get_columns(json_file_name)
    for each in column_names:
        try:
            element[each] = getattr(ents, each)
        except Exception:
            print each + ' not found in entities! Sorry. '
    return element


#######              json_object           #######
#  it is essentially same form as template.json  #

def some_funct(json_object, id):
    column_names, column_types = reader.get_columns(json_file_name)
    if does_match(json_object, column_names):
        element = manage_element.get_element(json_db_file, id)
