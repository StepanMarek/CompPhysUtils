def save(dataset, writeLine, filename, writeHeaders=False, writeFooters=False):
    nrows = len(dataset[0])
    ncols = len(dataset)
    file = open(filename, "w+")
    if writeHeaders:
        headers = writeHeaders(dataset)
        if len(headers) > 0:
            headers = headers + "\n"
        file.write(headers)
    for i in range(nrows):
        datarow = []
        for j in range(ncols):
            datarow.append(dataset[j][i])
        file.write(writeLine(datarow)+"\n")
    if writeFooters:
        footers = writeFooters(dataset)
        if len(footers) > 0:
            footers = footers + "\n"
        file.write(footers)
    file.close()

def datasetParse(savepointLines, context, dataset, writeLineFunctions, writeHeaderFunctions, writeFooterFunctions, defFilename="data.out"):
    # Parsers for the case when savepoint directive is provided at a given dataset - lacks one argument
    savepointSplit = savepointLines.split("\n")
    for i in range(len(savepointSplit)):
        savepointArgs = savepointSplit[i].split()
        if savepointArgs[0] == context:
            filename = defFilename
            if len(savepointArgs) > 2:
                filename = savepointArgs[2]
            # Save the dataset
            if not writeLineFunctions[savepointArgs[1]]:
                raise ValueError("No writeLine function defined for parser "+savepointArgs[1])
            save(dataset, writeLineFunctions[savepointArgs[1]], filename, writeHeaders=writeHeaderFunctions[savepointArgs[1]], writeFooters=writeFooterFunctions[savepointArgs[1]])

def parse(savepointLines, context, datasets, writeLineFunctions, writeHeaderFunctions, writeFooterFunctions, defFilename="data.out"):
    # Each line has following arguments - desired context, dataset name, parser with writeLine function, optional filename
    savepointSplit = savepointLines.split("\n")
    for i in range(len(savepointSplit)):
        savepointArgs = savepointSplit[i].split()
        if savepointArgs[0] == context:
            filename = defFilename
            if len(savepointArgs) > 3:
                filename = savepointArgs[3]
            # Save the dataset
            if not writeLineFunctions[savepointArgs[2]]:
                raise ValueError("No writeLine function defined for parser "+savepointArgs[2])
            save(datasets[savepointArgs[1]], writeLineFunctions[savepointArgs[2]], filename, writeHeaders=writeHeaderFunctions[savepointArgs[2]], writeFooters=writeFooterFunctions[savepointArgs[2]])
