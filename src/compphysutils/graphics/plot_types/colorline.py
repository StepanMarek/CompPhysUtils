import argparse

ap = argparse.ArgumentParser(description="Plots line with additional data shown as color.", prog="colorline")
ap.add_argument("--cmap", default="hot", help="Name of the colormap to use.")

def plot(datasets, axes, datasetLabels=False, **plotOptions):
    args = ap.parse_args(plotOptions["plotArgString"])
    if not datasetLabels:
        datasetLabels = [False]*len(datasets)
    for k in range(len(datasets)):
        if datasetLabels[k]:
            axes.colorline(datasets[k][0], datasets[k][1], datasets[k][2], linestyle=next(plotOptions["linestyleCycle"]), cmap=args.cmap, label=datasetLabels[k])
        else:
            axes.colorline(datasets[k][0], datasets[k][1], datasets[k][2], linestyle=next(plotOptions["linestyleCycle"]), cmap=args.cmap)
    return axes
