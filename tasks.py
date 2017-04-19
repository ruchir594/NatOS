# tasks.py

import tasktiger
tiger = tasktiger.TaskTiger()

from ActionsA.nlg import speak

@tiger.task()
def my_task(name):
    print('Hello', name)
    speak.say('Hello '+name)
