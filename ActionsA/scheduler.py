# scheduler.py

from tasks import tiger, my_task, push, execute
from tasktiger import Task
import json
import datetime
from bson import json_util

#task = Task(tiger, my_task, (['ruchir']))
#print task.delay(when=datetime.timedelta(seconds = 5))
def message(**kwargs):
    refs = ['seconds', 'minutes', 'hours', 'days']
    ref = ''
    val = ''
    text = ''
    player = ''
    command = ''
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if key in refs:
                ref = key
                val = value
            if key == 'text':
                text = value
            if key == 'command':
                command = value
            if key == 'player':
                player = value
    if text != '' and player != '':
        task = Task(tiger, push, ([text, player]))
        print task.delay(when=datetime.timedelta(**{ref: val}))
        print 'task player... ', task._queue, task._state, task._ts, task.id
    elif text != '':
        task = Task(tiger, push, ([text]))
        print task.delay(when=datetime.timedelta(**{ref: val}))
        print 'task... ', task._queue, task._state, task._ts
    if command != '':
        task = Task(tiger, execute, ([command]))
        print task.delay(when=datetime.timedelta(**{ref: val}))

def reminders(**kwargs):
    freq = ['everyday']
    var_freq = 0
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if key == 'frequency':
                var_freq = 1
            if key == 'dobj':
                blink = value
        if blink and var_freq == 1:
            message(seconds=5, text=blink.converse2('per1'))
            message(seconds=10, text=blink.converse2('per2'))
    return
