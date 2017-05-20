#!/usr/bin/python

import sys
sys.path.insert(0,'.')
import re

#from ActionsA import scheduler
#from ActionsA.nlg import speak
from ActionsA.nlg import generate
from ActionsA import scheduler

def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def lambda_function(a):
    print 'in here'
    chatbot = generate.generate(path = './Modules/MotivationBot/conversation.csv')
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
    return ret


#scheduler.message(seconds=4, text='Nitesh is brilliant...', command='python 334.py', player='afplay')
#scheduler.message(seconds=7, command='afplay ../Chained\ to\ the\ Rhythm.mp3')
