import argparse

ap = argparse.ArgumentParser(description="Plots line with additional data shown as color.", prog="colorline")
ap.add_argument("--cmap", default="hot", help="Name of the colormap to use.")
ap.add_argument("--vmin", default=False, help="Minimum value for colorbar.")
ap.add_argument("--vmax", default=1.0, help="Maximum value for colorbar.")
ap.add_argument("--norm", default="log", choices=["lin", "log"], help="Normalisation")

def plot(datasets, axes, datasetLabels=False, **plotOptions):
    args = ap.parse_args(plotOptions["plotArgString"])
    if not datasetLabels:
        datasetLabels = [False]*len(datasets)
    vrange = [args.vmin, args.vmax]
    if not args.vmin:
        if args.norm == "lin":
            vrange[0] = 0
        else:
            # TODO : Guess something better, based on values?
            vrange[0] = 1e-10
    for k in range(len(datasets)):
        if datasetLabels[k]:
            axes.colorline(datasets[k][0], datasets[k][1], datasets[k][2], linestyle=next(plotOptions["linestyleCycle"]), cmap=args.cmap, label=datasetLabels[k], vmin=vrange[0], vmax=vrange[1], norm=args.norm)
        else:
            axes.colorline(datasets[k][0], datasets[k][1], datasets[k][2], linestyle=next(plotOptions["linestyleCycle"]), cmap=args.cmap, vmin=vrange[0], vmax=vrange[1], norm=args.norm)
    return axes
