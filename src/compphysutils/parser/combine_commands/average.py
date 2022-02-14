import argparse

averageAP = argparse.ArgumentParser()
averageAP.add_argument("--stderr", action="store_true", help="If given, second column of the new dataset includes standard error given by the average. Need at least two averaging datasets.")
averageAP.add_argument("new_name", help="Name of the dataset containing the averaged values.")
averageAP.add_argument("datasets_to_average", nargs="+", help="Datasets that are to be averaged, elementwise in each column. Number of columns is given by the first dataset.")

def command(datasets, commandArgs):
    args = averageAP.parse_args(commandArgs)
    averages = []
    stderrs = []
    ncols = len(datasets[args.datasets_to_average[0]])
    nrows = len(datasets[args.datasets_to_average[0]][0])
    N = len(args.datasets_to_average)
    for i in range(ncols):
        averages.append([])
        stderrs.append([])
    for rowIndex in range(nrows):
        for colIndex in range(ncols):
            sumLin = 0
            sumSq = 0
            for datasetName in args.datasets_to_average:
                sumLin += datasets[datasetName][colIndex][rowIndex]
                sumSq += datasets[datasetName][colIndex][rowIndex] ** 2
            averages[colIndex].append(sumLin / N)
            if args.stderr:
                stderrs[colIndex].append(((sumSq / N - averages[colIndex][rowIndex] ** 2)/(N-1)) ** 0.5)
    datasets[args.new_name] = []
    for i in range(ncols):
        datasets[args.new_name].append(averages[i])
        if args.stderr:
            datasets[args.new_name].append(stderrs[i])
    return datasets
