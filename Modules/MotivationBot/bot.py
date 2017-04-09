import sys
sys.path.insert(0, '../../ActionsA')
from nle.naive_entities import *
from nlg.generate import *

a = ner_primitive('How do you do?')
#a.view() 
bot = generate('./conversation.csv')
print bot.converse2('Thank you')
