import sys
from os import path
 # add all the modules in it's lifetime to the path, failsafe for others
CURRENT_DIR = path.join(path.abspath(path.dirname(__file__)))
ACTIONS_A = path.join(CURRENT_DIR, "ActionsA")
sys.path.append(CURRENT_DIR)
sys.path.append(ACTIONS_A)


from natlib import *

pipeline = Pipeline()

# Modules Path: Directory where all the modules/apps are present!
MODULES_DIRECTORY = path.join(path.abspath(path.dirname(__file__)), "modules")

# Import Map: Map of the module with their entrypoint!
IMPORTMAPS = path.join(MODULES_DIRECTORY, "import.map")

autoload(IMPORTMAPS)