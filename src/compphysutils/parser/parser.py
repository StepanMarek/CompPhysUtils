from .post_processor import postProcessCommands
from .savepoint import handleSavepoints
from .. import __user_conf_dir
import configparser
import os
import sys
import importlib
import re

parserModules = {}
# Check for custom parser modules
customParsers = []
if os.path.isdir(os.path.expanduser(__user_conf_dir+"/parsers")):
    root, _, filenames = next(os.walk(os.path.expanduser(__user_conf_dir+"/parsers")))
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
readLineFunctions = {}
writeLineFunctions = {}
readFileFunctions = {}
writeFileFunctions = {}
readHeaderFunctions = {}
writeHeaderFunctions = {}
readFooterFunctions = {}
writeFooterFunctions = {}
readArgDefaults = {}
writeArgDefaults = {}
initReadObjects = {}
initWriteObjects = {}
for parserName in parserModules:
    # Prefer line-by-line reading when possible
    if hasattr(parserModules[parserName], "line"):
        readLineFunctions[parserName] = parserModules[parserName].line
    elif hasattr(parserModules[parserName], "file"):
        readFileFunctions[parserName] = parserModules[parserName].file
        readLineFunctions[parserName] = False
    else:
        # Neither line nor file reading utility provided, exception
        raise ModuleNotFoundError("Neither file nor line functions found for parser "+parserName+"!")
    if hasattr(parserModules[parserName], "writeLine"):
        writeLineFunctions[parserName] = parserModules[parserName].writeLine
    else:
        writeLineFunctions[parserName] = False
    if hasattr(parserModules[parserName], "writeFile"):
        writeFileFunctions[parserName] = parserModules[parserName].writeFile
    else:
        writeFileFunctions[parserName] = False
    if hasattr(parserModules[parserName], "argDefaults"):
        readArgDefaults[parserName] = parserModules[parserName].argDefaults
    else:
        readArgDefaults[parserName] = ""
    if hasattr(parserModules[parserName], "writeArgDefaults"):
        writeArgDefaults[parserName] = parserModules[parserName].writeArgDefaults
    else:
        writeArgDefaults[parserName] = ""
    if hasattr(parserModules[parserName], "initParserObjects"):
        initReadObjects[parserName] = parserModules[parserName].initParserObjects
    else:
        initReadObjects[parserName] = False
    if hasattr(parserModules[parserName], "initWriterObjects"):
        initWriteObjects[parserName] = parserModules[parserName].initWriterObjects
    else:
        initWriteObjects[parserName] = False
    if hasattr(parserModules[parserName], "readHeaders"):
        readHeaderFunctions[parserName] = parserModules[parserName].readHeaders
    else:
        readHeaderFunctions[parserName] = False
    if hasattr(parserModules[parserName], "readFooters"):
        readFooterFunctions[parserName] = parserModules[parserName].readFooters
    else:
        readFooterFunctions[parserName] = False
    if hasattr(parserModules[parserName], "writeHeaders"):
        writeHeaderFunctions[parserName] = parserModules[parserName].writeHeaders
    else:
        writeHeaderFunctions[parserName] = False
    if hasattr(parserModules[parserName], "writeFooters"):
        writeFooterFunctions[parserName] = parserModules[parserName].writeFooters
    else:
        writeFooterFunctions[parserName] = False

def readFile(filename, filetype, parserArgs=False):
    """
    Reads the file with given filetype parser and parserArgs

    First, generates the reader objects from parserArgs. Then, splits into two possibilities:
    If line reader is present, iterates line by line. Starts with header reader, if present, until
    it throws ValueError. Then it continues to line reader. Each line should be converted to set of values
    of the same size for each line. False is returned if the line is to be skipped. ValueError is to
    be thrown if going to footer reader is required. Footer reader is the last stage. On the other hand,
    if line reader is not present, default to file reader. There, leave file opening to the parser, only parse
    filename and objects. Expect the entire dataset returned.
    """
    # Allow for default arguments
    if not parserArgs:
        parserArgs = readArgDefaults[filetype]
    # Initiate reading objects
    if initReadObjects[filetype]:
        readerObjects = initReadObjects[filetype](parserArgs.split())
    else:
        readerObjects = []
    # Check whether reading line by line is present, as it is preferred
    if readLineFunctions[filetype]:
        # read lines
        # requires text mode
        with open(filename, "r") as f:
            # Read headers, until False is produced
            if readHeaderFunctions[filetype]:
                for line in f:
                    try:
                        readHeaderFunctions[filetype](line, *readerObjects)
                    except ValueError:
                        # Value error signals that it is time to move to main content reading
                        break
            # Finished reading headers, read main content
            dataset = []
            for line in f:
                try:
                    datarow = readLineFunctions[filetype](line, *readerObjects)
                    if datarow:
                        # Either initiate dataset or append datarow
                        if len(datarow) > len(dataset):
                            for dataitem in datarow:
                                dataset.append([dataitem])
                        else:
                            for i in range(len(datarow)):
                                dataset[i].append(datarow[i])
                    else:
                        continue
                except ValueError:
                    # Time to read footers
                    break
            # Finished reading main content, read footers
            if readFooterFunctions[filetype]:
                for line in f:
                    readFooterFunctions[filetype](line, *readerObjects)
            # Done
        return dataset
    else:
        # Read whole file in one go
        return readFileFunctions[filetype](filename, *readerObjects)

def writeFile(filename, filetype, dataset, parserArgs=False):
    # Initialize parserArgs
    if not parserArgs:
        parserArgs = writeArgDefaults[filetype]
    # Start by initialising writer objects
    if initWriteObjects[filetype]:
        writerObjects = initWriteObjects[filetype](parserArgs.split())
    else:
        writerObjects = []
    # Differentiate between line-by-line writing and all-in-one writing
    if writeLineFunctions[filetype]:
        # Write line by line
        # If filename is false, write to stdout
        if not filename:
            f = sys.stdout
        else:
            f = open(filename, "w+")
        # Start by writing headers
        # Headers/footers can be written all-in-one always
        if writeHeaderFunctions[filetype]:
            headers = writeHeaderFunctions[filetype](dataset, *writerObjects)
            if len(headers) > 0:
                headers += "\n"
            f.write(headers)
        # Continue with lines
        for i in range(len(dataset[0])):
            datarow = []
            for j in range(len(dataset)):
                datarow.append(dataset[j][i])
            line = writeLineFunctions[filetype](datarow, *writerObjects)
            f.write(line+"\n")
        # Finish by writing footers
        if writeFooterFunctions[filetype]:
            footers = writeFooterFunctions[filetype](dataset, *writerObjects)
            if len(footers) > 0:
                footers += "\n"
            f.write(footers)
        if filename:
            f.close()
    else:
        # Write all-in-one
        writeFileFunctions[filetype](filename, dataset, *writerObjects)

def postProcess(datagroups, command, args):
   return postProcessCommands[command](datagroups, args)

def save(savepointGroup, context, datasets, defaultDatasetName=False):
    toSave = handleSavepoints(savepointGroup, context, defaultDatasetName)
    for savepointArgs in toSave:
        writeFile(savepointArgs["filename"], savepointArgs["parserName"], datasets[savepointArgs["datasetName"]], savepointArgs["parserArgs"])

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
                datasets[datasetName] = readFile(cfg[groupName]["file"], cfg[groupName]["filetype"], parserArgs=parserArgs)
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
                save(cfg[groupName].get("savepoint"), "load", datasets, datasetName)
            if "post-process" in cfg[groupName]:
                differentCommands = cfg[groupName].get("post-process").split("\n")
                for commandLine in differentCommands:
                    commandSplit = commandLine.split()
                    if len(commandSplit) > 1:
                        datasets[datasetName] = postProcess(datasets[datasetName], commandSplit[0], commandSplit[1:])
                    else:
                        datasets[datasetName] = postProcess(datasets[datasetName], commandSplit[0], [])
            if "savepoint" in cfg[groupName]:
                save(cfg[groupName].get("savepoint"), "post-process", datasets, datasetName)
    return datasets
