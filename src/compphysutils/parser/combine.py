import importlib
import os
from .parser import parseDatasetConfig
from .parser import writeParseFunctions
from .parser import writeHeaderFunctions
from .parser import writeFooterFunctions
from .savepoint import parse as savepointParse

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

def runGroupData(cfg, datasets, cfgFileName):
    if "data" in cfg:
        # First, load data from datasetfiles
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
            datasets = commands[commandName](datasets, commandSplitLine[1:])
    # Finally, handle savepoint in the combine context
    if "savepoint" in cfg["data"]:
        savepointParse(cfg["data"].get("savepoint"), "combine", datasets, writeParseFunctions, writeHeaderFunctions, writeFooterFunctions, "data_combine.out")
    # End by returning the (changed) datasets
    return datasets
