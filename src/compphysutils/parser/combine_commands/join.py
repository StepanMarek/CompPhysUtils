import argparse

joinAP = argparse.ArgumentParser()
joinAP.add_argument("new_name", help="Name of the joined dataset.")
joinAP.add_argument("datasets_to_join", nargs="+", help="Datasets which will constitute the columns of the new dataset.")
def command(datasets, commandArgs):
    args = joinAP.parse_args(commandArgs)
    newDataset = []
    for elementName in args.datasets_to_join:
        for i in range(len(datasets[elementName])):
            newDataset.append(datasets[elementName][i])
    datasets[args.new_name] = newDataset
    return datasets
