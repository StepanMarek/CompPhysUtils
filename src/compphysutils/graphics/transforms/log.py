import argparse
import math

logTransAP = argparse.ArgumentParser()
logTransAP.add_argument("dataset_name", help="Name of the dataset.")
logTransAP.add_argument("column_index", type=int, help="Index of the column in the dataset.")
logTransAP.add_argument("--err", type=int, help="Do also an error calculation, on a different column.", default=False)
def command(datasets, argsString):
    args = logTransAP.parse_args(argsString)
    for i in range(len(datasets[args.dataset_name][args.column_index])):
        origX = datasets[args.dataset_name][args.column_index][i]
        datasets[args.dataset_name][args.column_index][i] = math.log(origX)
        if args.err:
            datasets[args.dataset_name][args.err][i] = abs(math.log(origX + datasets[args.dataset_name][args.err][i]) - math.log(origX))
    return datasets
