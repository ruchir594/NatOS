import requests, json
import nlu.element_man, nlu.action_header, nlu.state_update
import nle.entities
import jsondb.manage_element

json_template_file = 'template.json'
json_db_file = 'data.json'

def parse_text(each_ex, state = None):
    if state == 0:
        from spacy.en import English
        from nle import get_dependency, get_postagging, get_ner
        parser = English()
        parsedEx = parser(each_ex)
        # extract POS tagging from the parsed response
        full_pos = get_postagging(parsedEx)
        # extract dependency tree from parsed response
        full_dep = get_dependency(parsedEx)
        # extract tagged entities from parsed response
        full_ents = get_ner(each_ex,parsedEx)
        return full_pos, full_dep, full_ents
    if state == 1:
        r = requests.get("http://ec2-54-200-198-248.us-west-2.compute.amazonaws.com:5940/?message="+each_ex)
        #print r.status_code
        #print r.headers
        #print r.text
        parsedEx = json.loads(r.text)
        full_pos = parsedEx['full_pos']
        full_dep = parsedEx['full_dep']
        full_ents = parsedEx['full_ents']
        return full_pos, full_dep, full_ents
    print "parse parameter in parent.py missing"
    return None

def get_intents(example, full_pos, full_dep, full_ents, id):
    root_word = ''
    #action_points = get_action_points()
    for each_dep in full_dep:
        if each_dep[1] == 'ROOT':
            root_word = each_dep[0].lower()
    a = ner(example, full_pos, full_ents)
    print root_word
    print a.view()
    #actions_on = get_actions_on(a)
    example = example.lower()

def local_cmd_testing():
    example = ["I just want to buy some cake today around 6 pm"]
    for each_ex in example:
        print '-------------------------'
        print each_ex
        id = '104'
        each_ex = unicode(each_ex, "utf-8")
        # locally parsed from spacy
        full_pos, full_dep, full_ents = parse_text(each_ex, 1)
        # get words from action points
        #action_points = get_action_points()
        # find root word from dependency
        root_word = ''
        for each_dep in full_dep:
            if each_dep[1] == 'ROOT':
                root_word = each_dep[0].lower()
        # tag entities using local NER
        a = nle.entities.ner(example, full_pos, full_ents)
        #print root_word
        #print a.view()
        print a.day, a.location
        element = jsondb.manage_element.get_element(json_db_file, id)
        print element
        element = nlu.element_man.fill_element(element, a)
        print element
        jsondb.manage_element.update_element(json_db_file, element)
        print nlu.action_header.get_action_params_id(element)

local_cmd_testing()
