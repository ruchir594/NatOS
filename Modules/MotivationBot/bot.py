import sys
sys.path.insert(0,'.')

from ActionsA import scheduler
from ActionsA.nlg import speak

def lambda_function(a):
    return a

scheduler.message(seconds=4, text='Nitesh is brilliant...')
