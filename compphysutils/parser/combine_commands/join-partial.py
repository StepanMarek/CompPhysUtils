import argparse
from ..parser import parse_ranges, ranges_to_indices

joinAP = argparse.ArgumentParser(prog="join-partial", description="Joins chosen columns from different datasets into a new dataset.")
joinAP.add_argument("new_name", help="Name of the joined dataset.")
joinAP.add_argument("col_doubles", nargs="+", help="Dataset name and range of columns to join. Here, range is specified as union of slices, e.g. 1,2:4,6:-1:2")

def command(datasets, commandArgs):
    args = joinAP.parse_args(commandArgs)
    if len(args.col_doubles) % 2 != 0:
        raise ValueError("Incorrect column coordinates for join-partial.")
    newDataset = []
    for i in range(0, len(args.col_doubles), 2):
        cols = ranges_to_indices(parse_ranges(args.col_doubles[i+1]), datasets[args.col_doubles[i]])
        for j in cols:
            newDataset.append(datasets[args.col_doubles[i]][j])
    datasets[args.new_name] = newDataset
    return datasets
