import argparse

ap = argparse.ArgumentParser(prog="fill_between")
ap.add_argument("--fillBound", default=0, type=float, help="Bound to which to fill the line. Is not used when two lines are provided.")

def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    # Default base is 10
    if not datasetLabels:
        datasetLabels = [False] * len(datasets)
    args = ap.parse_args(plotOptions["plotArgString"])
    for dataIndex in range(len(datasets)):
        if len(datasets[dataIndex]) == 3:
            axisObj.fill_between(datasets[dataIndex][0], datasets[dataIndex][1], datasets[dataIndex][2], color=next(plotOptions["colorCycle"]))
        else:
            # Fill between given value
            axisObj.fill_between(datasets[dataIndex][0], args.fillBound, datasets[dataIndex][1], color=next(plotOptions["colorCycle"]))
    return axisObj
