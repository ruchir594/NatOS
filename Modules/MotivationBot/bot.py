import sys
sys.path.insert(0, '../../ActionsA')
from nle.naive_entities import *

a = ner_primitive('How do you do?')
a.view()
