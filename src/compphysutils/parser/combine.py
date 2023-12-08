import importlib
import os
from . import save, parseDatasetConfig
from .. import __user_conf_dir

## Search for default combine commands
roots = []
modFilenames = []
root, _, filenames = next(os.walk(os.path.dirname(__file__)+"/combine_commands"))
roots.append(root)
modFilenames.append(filenames)
## Search for custom combine commands
if os.path.isdir(os.path.expanduser(__user_conf_dir+"/combine_commands")):
    root, _, filenames = next(os.walk(os.path.expanduser(__user_conf_dir+"/combine_commands")))
    roots.append(root)
    modFilenames.append(filenames)
## Import all commands
## Defer load for when it will be used
commandModules = {}
commands = {}
for i in range(len(roots)):
    for filename in modFilenames[i]:
        commandName = filename.split(".")[0]
        if commandName[0:2] == "__":
            # Skip __init__.py and similar commands
            continue
        spec = importlib.util.spec_from_file_location("compphysutils.parser.combine_commands."+commandName, roots[i]+"/"+filename)
        mod = importlib.util.module_from_spec(spec)
        commandModules[commandName] = {"spec" : spec, "module" : mod, "loaded" : False}
        #spec.loader.exec_module(mod)
        #commands[commandName] = mod.command

def runGroupData(cfg, datasets, cfgFileName):
    if "data" in cfg:
        # First, load data from datasetfiles
        # This way, same definitions can be used for different datasets
        # TODO : Add to documentation
        datasetfiles = cfg["data"].get("datasetfiles", False)
        if datasetfiles:
            for datasetFileName in datasetfiles.split():
                datasets.update(parseDatasetConfig(datasetFileName))
    # If there are in place defined datasets, they take priority
    datasets.update(parseDatasetConfig(cfgFileName))
    # If there is no data group, this is all that is done
    if not "data" in cfg:
        return datasets
    # Now, progress to the combine command
    if "combine" in cfg["data"]:
        combineCommands = cfg.get("data", "combine").split("\n")
        for commandLine in combineCommands:
            commandSplitLine = commandLine.split()
            commandName = commandSplitLine[0]
            if not commandName in commandModules:
                raise ModuleNotFoundError("Combine command "+commandName+" not found in the search tree!")
            if not commandModules[commandName]["loaded"]:
                commandModules[commandName]["spec"].loader.exec_module(commandModules[commandName]["module"])
                commandModules[commandName]["loaded"] = True
                commands[commandName] = commandModules[commandName]["module"].command
            datasets = commands[commandName](datasets, commandSplitLine[1:])
    # Finally, handle savepoint in the combine context
    if "savepoint" in cfg["data"]:
        save(cfg["data"].get("savepoint"), "combine", datasets)
    # End by returning the (changed) datasets
    return datasets
