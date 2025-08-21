import argparse

ap = argparse.ArgumentParser(prog="scatter", description="Scatter graph.")
ap.add_argument("--ms", default=20.0, type=float, help="Marker size.")

def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    args = ap.parse_args(plotOptions["plotArgString"])
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        axisObj.scatter(datasets[dataIndex][0], datasets[dataIndex][1], label=datasetLabels[dataIndex], c=next(plotOptions["colorCycle"]), marker=next(plotOptions["markerstyleCycle"]),
                        s=args.ms)
    return axisObj
