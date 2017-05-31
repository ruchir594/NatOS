#!/usr/bin/python

import sys
sys.path.insert(0,'.')
import re
import pickle
import os.path

#from ActionsA import scheduler
#from ActionsA.nlg import speak
from ActionsA.nlg import generate
from ActionsA import scheduler

thispath = './Modules/MotivationBot/'

def getWords(data):
    return re.compile(r"[\w']+").findall(data)


def lambda_function(a):
    # if chatbot instance doesnt exist, we make it.
    if not os.path.isfile(thispath+'motivationbot'):
        print 'building chatbot instance...'
        generate.build_lambda(thispath)
    # loading local chatbot instance so heavy processing must not be needed everytime
    f = open(thispath+'motivationbot', 'r')
    chatbot=pickle.load(f)
    # You code of handling stuff
    b = getWords(a)
    if a.find('help') != -1:
        rem1 = ['weight', 'calories', 'fit', 'eat', 'healthy', 'lean', 'thin', 'fat']
        if any(x in rem1 for x in b) == True:
            # this person wants help with
            # - losing his weight
            # - cutting down on calories
            # - stay lean and fit
            # - eating healthy
            ret = 'Okay, I will remind you.'
            scheduler.reminders(frequency='everyday', dobj=chatbot)
    else:
        ret = chatbot.converse2(a)
    return ret

#print lambda_function('hello hello')
#scheduler.message(seconds=4, text='Ruchir works', player='afplay')
#scheduler.message(seconds=4, text='Nitesh is brilliant...', command='python 334.py', player='afplay')
#scheduler.message(seconds=7, command='afplay ../Chained\ to\ the\ Rhythm.mp3')
