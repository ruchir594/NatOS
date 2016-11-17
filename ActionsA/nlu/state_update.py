import csv

state_user = 'state_user.csv'
state_transitions = 'state_transitions.csv'
delim = ','

def push_in_csv(user_id, start_state):
    with open(state_user, 'a') as csvfile:
        fieldnames = ['user_id', 'current_state']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'user_id': user_id, 'current_state': start_state})

def update_state_csv(user_id, new_state):
    file_su = csv.reader(open(state_user,"r"),delimiter=delim)
    arr = []
    for each in file_su:
        if each[0] == user_id:
            arr.append([each[0],new_state])
        else:
            arr.append([each[0],each[1]])
    with open(state_user, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for each in arr:
            spamwriter.writerow([each[0],each[1]])

def get_current_state_user(user_id, start_state = 'st001'):
    file_su = csv.reader(open(state_user,"r"),delimiter=delim)
    for row in file_su:
        if row[0] == user_id:
            return row[1]
    # if the user is new, i.e. no record of him is found, we push a new record for that id.
    push_in_csv(user_id, start_state)
    return start_state

def get_new_state(user_id, current_state, actions_on, action_params):
    file_su = csv.reader(open(state_transitions,"r"),delimiter=delim)
    for row in file_su:
        if row[:-1] == [current_state, actions_on, action_params]:
            update_state_csv(user_id, row[3])
            return row[3]
    return 'not found'

print get_current_state_user('104')
print get_new_state('104','st001', 'book', 'ap002')
