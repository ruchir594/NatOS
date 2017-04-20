#!/usr/bin/python
import sys
from os import environ, path
sys.path.append(path.join(path.dirname(path.abspath(__file__)), "ActionsA"))
from lib import tasktiger
from redis import Redis
import re

environ.update({
    "PYTHONPATH": "{0}{1}".format(environ["PYTHONPATH"] if "PYTHONPATH" in environ else "", ":" + path.dirname(path.join(path.abspath(__file__))))
})

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    conn = Redis(db=0, decode_responses=True)
    tiger = tasktiger.TaskTiger(connection=conn)
    tiger.run_worker()