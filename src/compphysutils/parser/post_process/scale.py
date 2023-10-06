import argparse

ap = argparse.ArgumentParser()
ap.add_argument("column", type=int, default=0, help="Number of the column to apply the scaling to. [default : 0]")
ap.add_argument("amount", type=float, default=1.0, help="Multiply all values in the given column by this value. [default : 1.0]")

def command(dataset, argString):
    # Output above and below in separate datasets
    newDataset = []
    args = ap.parse_args(argString)
    for i in range(len(dataset)):
        newDataset.append([])
        for j in range(len(dataset[i])):
            newDataset[i].append(dataset[i][j])
    for i in range(len(newDataset[args.column])):
        # Output the same dataset, but with opposite value in the given axis index
        newDataset[args.column][i] *= args.amount
    return newDataset
