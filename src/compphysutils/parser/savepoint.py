def save(dataset, writeLine, filename):
    nrows = len(dataset[0])
    ncols = len(dataset)
    file = open(filename, "w+")
    for i in range(nrows):
        datarow = []
        for j in range(ncols):
            datarow.append(dataset[j][i])
        file.write(writeLine(datarow)+"\n")
    file.close()

def datasetParse(savepointLines, context, dataset, writeLineFunctions, defFilename="data.out"):
    # Parsers for the case when savepoint directive is provided at a given dataset - lacks one argument
    savepointSplit = savepointLines.split("\n")
    for i in range(len(savepointSplit)):
        savepointArgs = savepointSplit[i].split()
        if savepointArgs[0] == context:
            filename = defFilename
            if len(savepointArgs) > 2:
                filename = savepointArgs[2]
            # Save the dataset
            save(dataset, writeLineFunctions[savepointArgs[1]], filename)

def parse(savepointLines, context, datasets, writeLineFunctions, defFilename="data.out"):
    # Each line has following arguments - desired context, dataset name, parser with writeLine function, optional filename
    savepointSplit = savepointLines.split("\n")
    for i in range(len(savepointSplit)):
        savepointArgs = savepointSplit[i].split()
        if savepointArgs[0] == context:
            filename = defFilename
            if len(savepointArgs) > 3:
                filename = savepointArgs[3]
            # Save the dataset
            save(datasets[savepointArgs[1]], writeLineFunctions[savepointArgs[2]], filename)
