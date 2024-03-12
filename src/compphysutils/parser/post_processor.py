import os
from .. import __user_conf_dir
import importlib.util

## Search for default post-processing commands
roots = []
modFilenames = []
root, _, filenames = next(os.walk(os.path.dirname(__file__)+"/post_process"))
roots.append(root)
modFilenames.append(filenames)
## Search for custom post_process commands
if os.path.isdir(os.path.expanduser(__user_conf_dir+"/post_process")):
    root, _, filenames = next(os.walk(os.path.expanduser(__user_conf_dir+"/post_process")))
    roots.append(root)
    modFilenames.append(filenames)
## Import all commands
postProcessCommands = {}
for i in range(len(roots)):
    for filename in modFilenames[i]:
        commandName = filename.split(".")[0]
        if commandName[0:2] == "__":
            # Skip __init__.py and similar commands
            continue
        spec = importlib.util.spec_from_file_location("compphysutils.parser.post_process."+commandName, roots[i]+"/"+filename)
        mod = importlib.util.module_from_spec(spec)
        postProcessCommands[commandName] = {"spec" : spec, "module" : mod, "loaded" : False}
