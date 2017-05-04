#!/usr/bin/python

import sys
sys.path.insert(0,'.')
import re
import random

#from ActionsA import scheduler
#from ActionsA.nlg import speak
from ActionsA.nlg import generate
from ActionsA import scheduler

def lambda_function(a):
    chatbot = generate.generate_lines('./Modules/joke/conversation.txt')
    return random.choice(chatbot)
