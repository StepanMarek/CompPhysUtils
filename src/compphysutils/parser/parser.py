from .post_processor import postProcessCommands
from .savepoint import datasetParse as savepointDatasetParse
import configparser
import os
import importlib
import re

parserModules = {}
# Check for custom parser modules
customParsers = []
if os.path.isdir(os.path.expanduser("~/.config/compphysutils/parsers")):
    root, _, filenames = next(os.walk(os.path.expanduser("~/.config/compphysutils/parsers")))
    customParsers = list(map(lambda f: root+"/"+f, filenames))
# Check for default parser modules
root, _, filenames = next(os.walk(os.path.dirname(__file__)+"/parsers"))
defaultParsers = list(map(lambda f: root+"/"+f, filenames))
# Ideally, custom parsers should overwrite default parsers, not sure if this works
rexp = re.compile(".*/(.*)\.py")
for parserFileName in (defaultParsers + customParsers):
    parserType = rexp.search(parserFileName).group(1)
    if parserType[0:2] == "__":
        # Not a parser, but just a init or other module
        continue
    spec = importlib.util.spec_from_file_location("compphysutils.parser.parsers."+parserType, parserFileName)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    parserModules[parserType] = mod
lineParseFunctions = {}
writeParseFunctions = {}
writeHeaderFunctions = {}
writeFooterFunctions = {}
parserArgsDefaults = {}
initObjectsFunctions = {}
for parserName in parserModules:
    lineParseFunctions[parserName] = parserModules[parserName].line
    parserArgsDefaults[parserName] = parserModules[parserName].argDefaults
    initObjectsFunctions[parserName] = parserModules[parserName].initParserObjects
    if hasattr(parserModules[parserName], "writeLine"):
        writeParseFunctions[parserName] = parserModules[parserName].writeLine
    else:
        writeParseFunctions[parserName] = False
    if hasattr(parserModules[parserName], "writeHeaders"):
        writeHeaderFunctions[parserName] = parserModules[parserName].writeHeaders
    else:
        writeHeaderFunctions[parserName] = False
    if hasattr(parserModules[parserName], "writeFooters"):
        writeFooterFunctions[parserName] = parserModules[parserName].writeFooters
    else:
        writeFooterFunctions[parserName] = False

def parseFile(filename, filetype, parserArgs=False):
    if not parserArgs:
        parserArgs = parserArgsDefaults[filetype]
    file = open(filename, "r")
    datagroups = []
    parserObjects = initObjectsFunctions[filetype](parserArgs)
    currentParser = lineParseFunctions[filetype]
    for line in file:
        # Read line by line
        # Can return bool False if line is to be skipped
        readGroups = currentParser(line, *parserObjects)
        if readGroups:
            for i in range(len(readGroups)):
                if len(datagroups) > i:
                    datagroups[i].append(readGroups[i])
                else:
                    datagroups.append([readGroups[i]])
    file.close()
    return datagroups

def postProcess(datagroups, command, args):
   return postProcessCommands[command](datagroups, args)

def parseDatasetConfig(configFilename):
    cfg = configparser.ConfigParser()
    cfg.read(configFilename)
    datasets = {}
    for groupName in cfg.sections():
        if "dataset" in groupName:
            datasetName = groupName.split(".")[1]
            if "file" in cfg[groupName]:
                # Create datasets from file
                parserArgs = cfg[groupName].get("parser-args", False)
                datasets[datasetName] = parseFile(cfg[groupName]["file"], cfg[groupName]["filetype"], parserArgs=parserArgs)
            elif "list" in cfg[groupName]:
                # Create dataset from list, defaultly convert to float
                # TODO : Should there be som interface to different convertors?
                # A more sophisticated and decoupled list types
                splitList = cfg[groupName]["list"].split("\n")
                if "listtype" in cfg[groupName]:
                    if cfg[groupName]["listtype"] == "string":
                        datasets[datasetName] = list(map(lambda s: s.split(), splitList))
                    else:
                        datasets[datasetName] = list(map(lambda s: list(map(float, s.split())), splitList))
                else:
                    datasets[datasetName] = list(map(lambda s: list(map(float, s.split())), splitList))
            if "savepoint" in cfg[groupName]:
                savepointDatasetParse(cfg[groupName].get("savepoint"), "load", datasets[datasetName], writeParseFunctions, writeHeaderFunctions, writeFooterFunctions)
            if "post-process" in cfg[groupName]:
                commandSplit = cfg[groupName]["post-process"].split()
                if len(commandSplit) > 1:
                    datasets[datasetName] = postProcess(datasets[datasetName], commandSplit[0], commandSplit[1:])
                else:
                    datasets[datasetName] = postProcess(datasets[datasetName], commandSplit[0], [])
            if "savepoint" in cfg[groupName]:
                savepointDatasetParse(cfg[groupName].get("savepoint"), "post-process", datasets[datasetName], writeParseFunctions, writeHeaderFunctions, writeFooterFunctions, defFilename="data_post.out")
    return datasets
