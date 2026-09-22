import argparse

joinAP = argparse.ArgumentParser()
joinAP.add_argument("new_name", help="Name of the joined dataset.")
joinAP.add_argument("cols_to_join", nargs="+", help="Columns to be joined - always pair dataset name and column index. Can use '1:' etc. i.e. python slices")

def indicesFromSlice(sliceString, dataset):
    # Start by determining number of parameters
    split = sliceString.split(":")
    numArgs = len(split)
    if numArgs == 1:
        # Single column
        return [int(split[0])]
    if numArgs == 2:
        # Step = 1, unclear whether end is present
        if split[1] == "":
            # Create default end - end of dataset
            split[1] = len(dataset)
        return range(int(split[0]), int(split[1]))
    if numArgs == 3:
       # fully customized, assume all is defined
       return range(*map(int, split))

def command(datasets, commandArgs):
    args = joinAP.parse_args(commandArgs)
    if len(args.cols_to_join) % 2 != 0:
        raise ValueError("Incorrect column coordinates for join-partial.")
    newDataset = []
    for i in range(0, len(args.cols_to_join), 2):
        for j in indicesFromSlice(args.cols_to_join[i+1], datasets[args.cols_to_join[i]]):
            newDataset.append(datasets[args.cols_to_join[i]][j])
    datasets[args.new_name] = newDataset
    return datasets
