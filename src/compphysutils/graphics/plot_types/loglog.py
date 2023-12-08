import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--base", default=10, type=int, help="Base of the log scale, default is 10.")

def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    # Default base is 10
    if not datasetLabels:
        datasetLabels = [False] * len(datasets)
    args = ap.parse_args(plotOptions["plotArgString"])
    axisObj.set_xscale("log", base=args.base)
    axisObj.set_yscale("log", base=args.base)
    for dataIndex in range(len(datasets)):
        if len(datasets[dataIndex]) >= 4:
            axisObj.errorbar(datasets[dataIndex][0], datasets[dataIndex][2], xerr=datasets[dataIndex][1], yerr=datasets[dataIndex][3], capsize=4, lw=0, elinewidth=2, marker=".", label=datasetLabels[dataIndex], color=next(plotOptions["colorCycle"]))
        elif len(datasets[dataIndex]) >= 3:
            axisObj.errorbar(datasets[dataIndex][0], datasets[dataIndex][1], yerr=datasets[dataIndex][2], capsize=4, lw=0, elinewidth=2, marker=".", label=datasetLabels[dataIndex], color=next(plotOptions["colorCycle"]))
        else:
            # No errorbars
            axisObj.scatter(datasets[dataIndex][0], datasets[dataIndex][1], marker=".", label=datasetLabels[dataIndex], color=next(plotOptions["colorCycle"]))
    return axisObj
