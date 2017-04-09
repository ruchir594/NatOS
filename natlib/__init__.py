from os import listdir, path
from importlib import import_module

CURRENT_DIRECTORY = path.dirname(path.abspath(__file__))
_, PARENT_MODULE_NAME = path.split(CURRENT_DIRECTORY)
modules = [module.replace(".py", "") for module in listdir(CURRENT_DIRECTORY) if not module.startswith("_") and not module.startswith(".") and not module.endswith(".pyc")]
for module in modules:
    try:
        globals()[module] = getattr(import_module(".%s" % module, PARENT_MODULE_NAME), module)
    except AttributeError, e:
        globals()[module.title()] = getattr(import_module(".%s" % module, PARENT_MODULE_NAME), module.title())