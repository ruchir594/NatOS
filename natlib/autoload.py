import json
from os import path, listdir
import semver
from collections import OrderedDict
from importlib import import_module

from module_name import module_name

def autoload(map):
    MODULES_DIRECTORY = path.dirname(map)
    apps = OrderedDict()
    with open(map) as map_handler:
        schema = json.loads(map_handler.read())
    installed = [dir for dir in listdir(MODULES_DIRECTORY) if not dir.startswith(".") and not dir.endswith(".map")]
    for app in schema["apps"]:
        if app in installed:
            try:
                app_dir = path.join(MODULES_DIRECTORY, app)
                with open(path.join(app_dir, "specs.json")) as app_spec:
                    spec = json.loads(app_spec.read())
                version = schema["apps"][app]
                version_info = semver.parse_version_info(version)
                temp = apps[app] = {
                    "name": app,
                    "slug": module_name(app, version),
                    "version": version_info
                }
                temp["module"] = import_module(".{}".format(app), "modules")
            except ValueError, e:
                print "Cannot load the module " + str(e)

    print apps