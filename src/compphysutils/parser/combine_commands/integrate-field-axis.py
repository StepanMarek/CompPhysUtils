import argparse
import numpy as np

integrationAP = argparse.ArgumentParser()
integrationAP.add_argument("--axisIndex", type=int, help="Index of the axis over which to do the integration.")
integrationAP.add_argument("--boxSize", type=lambda x: list(map(int, x.split(","))), help="The dimensions (shape) of the array. In unrolled storage, first shape is the dimension of the outermost loop, last is the dimension of inner-most loop.")
integrationAP.add_argument("--ignoreCols", default=[], type=lambda x:list(map(int, x.split(","))), help="Given columns in the dataset will not be integrated - instead, they will be simply rolled back by the given axis.")
integrationAP.add_argument("newDataset", help="Name of the dataset where the integrated values will be saved.")
integrationAP.add_argument("xs", nargs=2, help="Column coordinates of the values of integration variable.")
integrationAP.add_argument("toIntegrate", help="Name of the dataset that contains the data to be integrated. Columns are integrated independently.")

def command(datasets, argsString):
    args = integrationAP.parse_args(argsString)
    # Do sanity checks
    if args.boxSize[args.axisIndex] != len(datasets[args.xs[0]][int(args.xs[1])]):
        raise ValueError("Cannot integrate along axis "+str(args.axisIndex)+" - axis size is "+str(args.boxSize[args.axisIndex])+" and provided x values have size "+str(len(datasets[args.xs[0]][int(args.xs[1])])))
    if np.prod(args.boxSize) != len(datasets[args.toIntegrate][0]):
        raise ValueError("Cannot integrate dataset "+args.toIntegrate+" - given boxSize requires size "+str(np.prod(args.boxSize))+" but the size of the dataset is "+str(len(datasets[args.toIntegrate][0])))
    # Start by reshaping the given arrays
    shapedColumns = []
    ignoredColumns = []
    columnMap = []
    for i in range(len(datasets[args.toIntegrate])):
        if i in args.ignoreCols:
            ignoredColumns.append(np.array(datasets[args.toIntegrate][i]).reshape(args.boxSize))
            columnMap.append("ignore")
        else:
            shapedColumns.append(np.array(datasets[args.toIntegrate][i]).reshape(args.boxSize))
            columnMap.append("integrate")
    # Cast shapedColumns to array itself
    shapedColumns = np.array(shapedColumns)
    # Carry out the integration, have to offset index by one, as outermost axis is now the axis of columns
    # TODO : Is it desirable to instead cast to lists?
    integratedColumns = np.trapz(shapedColumns, x=datasets[args.xs[0]][int(args.xs[1])], axis=args.axisIndex+1)
    # Ignored columns are just rolled back - for each, choose 0 index on the integrating axis
    for i in range(len(ignoredColumns)):
        ignoredColumns[i] = np.moveaxis(ignoredColumns[i], args.axisIndex, 0)[0]
    # Construct the final dataset
    datasets[args.newDataset] = []
    integratedIndex = 0
    ignoredIndex = 0
    for i in range(len(columnMap)):
        if columnMap[i] == "ignore":
            datasets[args.newDataset].append(ignoredColumns[ignoredIndex].flatten())
            ignoredIndex += 1
        else:
            datasets[args.newDataset].append(integratedColumns[integratedIndex].flatten())
            integratedIndex += 1
    return datasets
