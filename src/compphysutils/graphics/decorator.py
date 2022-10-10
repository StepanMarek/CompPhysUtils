import os
from .. import __user_conf_dir
import importlib

## Search for default post-processing commands
roots = []
modFilenames = []
root, _, filenames = next(os.walk(os.path.dirname(__file__)+"/decorate"))
roots.append(root)
modFilenames.append(filenames)
## Search for custom post_process commands
if os.path.isdir(os.path.expanduser(__user_conf_dir+"/decorate")):
    root, _, filenames = next(os.walk(os.path.expanduser(__user_conf_dir+"/decorate")))
    roots.append(root)
    modFilenames.append(filenames)
## Import all commands
decorations = {}
for i in range(len(roots)):
    for filename in modFilenames[i]:
        commandName = filename.split(".")[0]
        if commandName[0:2] == "__":
            # Skip __init__.py and similar commands
            continue
        spec = importlib.util.spec_from_file_location("compphysutils.graphics.decorate."+commandName, roots[i]+"/"+filename)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        decorations[commandName] = mod.command
