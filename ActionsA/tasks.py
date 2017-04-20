# tasks.py
from lib import tasktiger
from nlg.speak import say

tiger = tasktiger.TaskTiger()

say('damn')

@tiger.task()
def my_task(name):
    print('Hello', name)
    say('Hello '+name)

@tiger.task()
def push(line):
    print(line)
    say(line)
