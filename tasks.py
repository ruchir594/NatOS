# tasks.py

import tasktiger
tiger = tasktiger.TaskTiger()

@tiger.task()
def my_task(name):
    print('Hello', name)
