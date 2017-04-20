# scheduler.py

from tasks import tiger, my_task, push
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
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if key in refs:
                ref = key
                val = value
            if key == 'text':
                text = value

    task = Task(tiger, push, ([text]))
    print task.delay(when=datetime.timedelta(**{ref: val}))
