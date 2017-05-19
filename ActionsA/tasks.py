# tasks.py
from lib import tasktiger
from nlg.speak import say
import subprocess

tiger = tasktiger.TaskTiger()

#say('damn')

@tiger.task()
def push(line):
    print(line)
    say(line)

@tiger.task()
def execute(command):
    print(command)
    listen = subprocess.Popen(command, shell=True)


def my_task(name):
    print('Hello', name)
    say('Hello '+name)
