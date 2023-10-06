import argparse

def parseColRange(colRangeString):
    partialRanges = colRangeString.split(",")
    indices = []
    for partialRange in partialRanges:
        if partialRange.find(":") != -1:
            start, end = partialRange.split(":")
            indices = indices + list(range(int(start), int(end)))
        else:
            indices.append(int(partialRange))
    return indices

ap = argparse.ArgumentParser()
ap.add_argument("--colRange", type=parseColRange, default=False, help="Indices/ranges of columns that should be included in the union. Shared for all datasets. Format as '0:3,5', which implies include columns 0,1,2,5. Default : use all columns from first dataset given.")
ap.add_argument("new_name", help="Name of the dataset union.")
ap.add_argument("datasets", nargs="+", help="Names of datasets to use for the union.")

def command(datasets, commandArgs):
    args = ap.parse_args(commandArgs)
    datasets[args.new_name] = []
    indices = args.colRange
    if not indices:
        indices = range(len(datasets[args.datasets[0]]))
    for i in indices:
        datasets[args.new_name].append([])
        for j in range(len(args.datasets)):
            for k in range(len(datasets[args.datasets[j]][i])):
                datasets[args.new_name][-1].append(datasets[args.datasets[j]][i][k])
    return datasets
