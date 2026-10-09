import argparse
from ..parser import parse_ranges, ranges_to_indices

ap = argparse.ArgumentParser()
ap.add_argument("column", type=parse_ranges, default="0", help="Range of the columns to apply the scaling to. [default : 0]")
ap.add_argument("amount", type=float, default=1.0, help="Multiply all values in the given column by this value. [default : 1.0]")

def command(dataset, argString):
    # Output above and below in separate datasets
    newDataset = []
    args = ap.parse_args(argString)
    for i in range(len(dataset)):
        newDataset.append([])
        for j in range(len(dataset[i])):
            newDataset[i].append(dataset[i][j])
    scaled_cols = ranges_to_indices(args.column, newDataset)
    for i in scaled_cols:
        for j in range(len(newDataset[i])):
            # Scale the column
            newDataset[i][j] *= args.amount
    return newDataset
