from .post_process import postProcessCommands
import configparser
import os
import importlib

parserModules = {}
for parserFileName in os.listdir(os.path.dirname(__file__)+"/parsers"):
    if parserFileName[0:2] == "__":
        # Not a parser, but just a init or other module
        continue
    parserType = parserFileName.split(".")[0]
    parserModules[parserType] = importlib.import_module("compphysutils.parser.parsers."+parserType)
lineParseFunctions = {}
parserArgsDefaults = {}
initObjectsFunctions = {}
for parserName in parserModules:
    lineParseFunctions[parserName] = parserModules[parserName].line
    parserArgsDefaults[parserName] = parserModules[parserName].argDefaults
    initObjectsFunctions[parserName] = parserModules[parserName].initParserObjects
#lineParseFunctions = {"cols" : parserModules["cols"].colsLine}
#parserArgsDefaults = {"cols" : "0"}
#initObjectsFunctions = {"cols" : parserModules["cols"].initParserObjects}
#lineParseFunctions = {
#    "hlg" : hlgParser.hlgLine,
#    "aims" : aimsParser.aimsLine,
#    "eiger" : eigerParser.eigerLine,
#    "cols" : colsParser.colsLine
#}
#
#parserArgsDefaults = {
#    "hlg" : "--unit eV",
#    "aims" : "--unit eV",
#    "eiger" : "--unit eV",
#    "cols" : "0 1"
#}
#
#initObjectsFunctions = {
#    "hlg" : hlgParser.initParserObjects,
#    "aims" : aimsParser.initParserObjects,
#    "eiger" : eigerParser.initParserObjects,
#    "cols" : colsParser.initParserObjects
#}

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
