# scheduler.py

def datetime_handler(x):
    if isinstance(x, datetime.timedelta):
        return x.isoformat()
    raise TypeError("Unknown type")


from tasks import tiger, my_task, push
from tasktiger import Task
import json
import datetime
from bson import json_util
now = datetime.datetime.now()
now_plus_10 = now + datetime.timedelta(seconds = 5)
#task = Task(tiger, my_task, (['ruchir']))
#print task.delay(when=datetime.timedelta(seconds = 5))

def message(time, line):
    task = Task(tiger, push, ([line]))
    print task.delay(when=time)
