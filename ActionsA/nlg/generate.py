#from __future__ import print_function
from nltk_chat_util import Chat, reflections
import pickle

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
    # NLTK Chat pairs are written in a CSV file. Check out following link
    # http://www.nltk.org/_modules/nltk/chat/eliza.html

    # There is a custom nltk_chat_util file in this directory, which uses
    # modified converse function to find the best match.

    # NLTK simply matches the best string to respond in a very naive way
    # we are going to do a bit better, se NLU Autobot.py
    if path == 'undefined':
        raise NoPath('A path is necessary')
    try:
        with open(path) as fh:
            f = map(lambda x: x.split(","), filter(lambda x: (x != ""), fh.read().split("\n")))
        pairs = build_pairs(f)
        chatbot = Chat(pairs, reflections)
        return chatbot

    except Exception, e:
        raise NoFile(str(e))

def generate_lines(path = 'undefined'):
    if path == 'undefined':
        raise NoPath('A path is necessary')
    try:
        with open(path) as fh:
            line = fh.readlines()
            return line
    except Exception, e:
        raise NoFile(str(e))

def build_lambda(thispath, botname):
    chatbot = generate(path = thispath + 'conversation.csv')
    f = open(thispath+botname, 'w')
    pickle.dump(chatbot, f)
