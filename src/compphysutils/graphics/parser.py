from . import hlgParser
from . import aimsParser
from .post_process import postProcessCommands
import configparser
import os

lineParseFunctions = {
    "hlg" : hlgParser.hlgLine,
    "aims" : aimsParser.aimsLine
}

parserKwargsDefaults = {
    "hlg" : {
        "outputUnit" : "eV"
    },
    "aims" : {
        "outputUnit" : "eV"
    }
}

initObjectsFunctions = {
    "hlg" : hlgParser.initParserObjects,
    "aims" : aimsParser.initParserObjects
}

def parseFile(filename, filetype, parserKwargs=False):
    if not parserKwargs:
        parserKwargs = parserKwargsDefaults[filetype]
    file = open(filename, "r")
    datagroups = []
    parserObjects = initObjectsFunctions[filetype]()
    currentParser = lineParseFunctions[filetype]
    for line in file:
        # Read line by line
        # Can return bool False if line is to be skipped
        readGroups = currentParser(line, *parserObjects, **parserKwargs)
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
                parserKwargs = cfg.get(groupName, "parser-kwargs", fallback=False)
                datasets[datasetName] = parseFile(cfg[groupName]["file"], cfg[groupName]["filetype"], parserKwargs=parserKwargs)
            elif "list" in cfg[groupName]:
                # Create dataset from list, defaultly convert to float
                # TODO : Should there be som interface to different convertors?
                # A more sophisticated and decoupled list types
                if "listtype" in cfg[groupName]:
                    if cfg[groupName]["listtype"] == "string":
                        datasets[datasetName] = [cfg[groupName]["list"].split()]
                    else:
                        datasets[datasetName] = [list(map(float, cfg[groupName]["list"].split()))]
                else:
                    datasets[datasetName] = [list(map(float, cfg[groupName]["list"].split()))]
            if "post-process" in cfg[groupName]:
                commandSplit = cfg[groupName]["post-process"].split()
                if len(commandSplit) > 1:
                    datasets[datasetName] = postProcess(datasets[datasetName], commandSplit[0], commandSplit[1:])
                else:
                    datasets[datasetName] = postProcess(datasets[datasetName], commandSplit[0], [])
    return datasets
