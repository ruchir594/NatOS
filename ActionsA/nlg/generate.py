#from __future__ import print_function
from nltk_chat_util import Chat, reflections

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

def build_pairs(f):
    a=[]
    for each in f:
        a.append((each[0].replace('*', '(.*)').encode('string-escape'), tuple(each[1].split('^'))))
    return tuple(a)

def generate (path = 'undefined', sleepword = 'zebra'):
    if path == 'undefined':
        raise NoPath('A path is necessary')
    try:
        with open(path) as fh:
            f = map(lambda x: x.split(","), filter(lambda x: (x != ""), fh.read().split("\n")))
        pairs = build_pairs(f)
        chatbot = Chat(pairs, reflections)
        return chatbot

    except Exception, e:
        raise NoFile('File not found at ' + path + ' // or // ' + str(e))
