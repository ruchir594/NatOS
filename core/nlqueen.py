# this is from preliminary testing of NatOS

import re, datetime

def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def intent(a):
    words = getWords(a)
    time_text = ['time']
    for each in time_text:
        if each in words:
            now = datetime.datetime.now()
            res = 'It is ' + str(now.hour) + ' ' + str(now.minute)
            return res
    return a

def extract(a):
    res = intent(a)
    return res
