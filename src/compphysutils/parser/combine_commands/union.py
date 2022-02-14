import argparse

unionAP = argparse.ArgumentParser()
unionAP.add_argument("new_name", help="New name of the dataset")
unionAP.add_argument("datasets_to_merge", nargs="+", help="Datasets, whose columns are to be added together, in the given order. First dataset determines the number of columns.")
def command(datasets, commandArgs):
    args = unionAP.parse_args(commandArgs)
    ncols = len(datasets[args.datasets_to_merge[0]])
    newcols = []
    for i in range(ncols):
        newcols.append([])
        for datasetName in args.datasets_to_merge:
            newcols[i] = newcols[i] + datasets[datasetName][i]
    datasets[args.new_name] = newcols
    return datasets
