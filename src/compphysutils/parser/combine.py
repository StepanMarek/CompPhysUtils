import importlib
import os

## Search for default combine commands
roots = []
modFilenames = []
root, _, filenames = next(os.walk(os.path.dirname(__file__)+"/combine_commands"))
roots.append(root)
modFilenames.append(filenames)
## Search for custom combine commands
if os.path.isdir(os.path.expanduser("~/.config/compphysutils/combine_commands")):
    root, _, filenames = next(os.walk(os.path.expanduser("~/.config/compphysutils/combine_commands")))
    roots.append(root)
    modFilenames.append(filenames)
## Import all commands
commands = {}
for i in range(len(roots)):
    for filename in modFilenames[i]:
        commandName = filename.split(".")[0]
        if commandName[0:2] == "__":
            # Skip __init__.py and similar commands
            continue
        spec = importlib.util.spec_from_file_location("compphysutils.parser.combine_commands."+commandName, roots[i]+"/"+filename)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        commands[commandName] = mod.command
