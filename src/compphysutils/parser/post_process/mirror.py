import argparse

ap = argparse.ArgumentParser()
ap.add_argument("axisIndex", type=int, default=False, help="Index of the axis that is to be mirrored along the origin plane.")

def command(dataset, argString):
    # Output above and below in separate datasets
    newDataset = []
    args = ap.parse_args(argString)
    for i in range(len(dataset)):
        newDataset.append([])
        for j in range(len(dataset[i])):
            newDataset[i].append(dataset[i][j])
    for i in range(len(dataset[args.axisIndex])):
        # Output the same dataset, but with opposite value in the given axis index
        newDataset[args.axisIndex][i] *= -1
    return newDataset
