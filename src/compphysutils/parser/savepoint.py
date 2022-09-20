shortContexts = ["load", "post-process"]

def parseArgs(savepointArgString, context, defaultDatasetName=False):
    result = {}
    savepointArgs = savepointArgString.split()
    result["context"] = savepointArgs[0]
    parserArgsStartIndex = 3
    # If the context is short, expect no dataset name - it needs to be provided by program
    if result["context"] in shortContexts:
        if not defaultDatasetName:
            raise ValueError("Invoking savepoint at short context but not providing default dataset name!")
        else:
            # Dataset name defined, proceed with parsing
            result["datasetName"] = defaultDatasetName
            result["parserName"] = savepointArgs[1]
            # Change parser start index
            parserArgsStartIndex = 2
    else:
        # Lond context
        result["datasetName"] = savepointArgs[1]
        result["parserName"] = savepointArgs[2]
    # Check for index before filename
    try:
        filenameSeparatorIndex = savepointArgs.index("--")
    except ValueError:
        filenameSeparatorIndex = -1
    if filenameSeparatorIndex == -1:
        # No filename, go to default filename
        result["filename"] = result["context"] + ".out"
        # If there is a single extra arg after parserName, assume it is also fileName
        if len(savepointArgs) == parserArgsStartIndex+1:
            result["filename"] = savepointArgs[parserArgsStartIndex]
            filenameSeparatorIndex = parserArgsStartIndex
    else:
        result["filename"] = savepointArgs[filenameSeparatorIndex+1]
    # Finally, determine parser args
    if filenameSeparatorIndex != -1:
        parserArgs = savepointArgs[parserArgsStartIndex:filenameSeparatorIndex]
    else:
        parserArgs = savepointArgs[parserArgsStartIndex:]
    result["parserArgs"] = parserArgs
    return result

def handleSavepoints(savepointGroup, context, defaultDatasetName=False):
    results = []
    for savepointArgs in savepointGroup.split("\n"):
        # Get parser arguments
        partialResult = parseArgs(savepointArgs, context, defaultDatasetName=defaultDatasetName)
        if partialResult["context"] == context:
            results.append(partialResult)
    return results

