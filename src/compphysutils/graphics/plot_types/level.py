import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--linelength", default=1.0, type=float, help="Length of the line marking the level.")

def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    args = ap.parse_args(plotOptions["plotArgString"])
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        # For x positions, only takes into account first element
        axisObj.eventplot(datasets[dataIndex][1], lineoffsets=datasets[dataIndex][0][0], linelengths=args.linelength, orientation="vertical", label=datasetLabels[dataIndex], colors=next(plotOptions["colorCycle"]))
    return axisObj
