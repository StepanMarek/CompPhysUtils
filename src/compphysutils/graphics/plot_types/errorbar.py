import argparse

ap = argparse.ArgumentParser(prog="errorbar", description="Plot scatter with error bounds.")
ap.add_argument("--lineWidth", default=0, type=float, help="Width of the line joining the points. [default : 0]")
ap.add_argument("--elineWidth", default=2, type=float, help="Width of the error bar line. [default : 2]")
ap.add_argument("--singleErr", default="y", choices=["x", "y"], help="When only a single error set is provided, which coordinate it corresponds to.")

def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    args = ap.parse_args(plotOptions["plotArgString"])
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        if len(datasets[dataIndex]) >= 4:
            # If at least four columns provided, plot errors on both axes
            axisObj.errorbar(datasets[dataIndex][0],
                             datasets[dataIndex][2],
                             xerr=datasets[dataIndex][1],
                             yerr=datasets[dataIndex][3],
                             capsize=4,
                             lw=args.lineWidth,
                             elinewidth=args.elineWidth,
                             marker=next(plotOptions["markerstyleCycle"]),
                             label=datasetLabels[dataIndex],
                             color=next(plotOptions["colorCycle"]))
        else:
            # Otherwise, just plot one error
            if args.singleErr == "x":
                axisObj.errorbar(datasets[dataIndex][0],
                                 datasets[dataIndex][1],
                                 xerr=datasets[dataIndex][2],
                                 capsize=4,
                                 lw=args.lineWidth,
                                 elinewidth=args.elineWidth,
                                 marker=next(plotOptions["markerstyleCycle"]),
                                 label=datasetLabels[dataIndex],
                                 color=next(plotOptions["colorCycle"]))
            else:
                axisObj.errorbar(datasets[dataIndex][0],
                                 datasets[dataIndex][1],
                                 yerr=datasets[dataIndex][2],
                                 capsize=4,
                                 lw=args.lineWidth,
                                 elinewidth=args.elineWidth,
                                 marker=next(plotOptions["markerstyleCycle"]),
                                 label=datasetLabels[dataIndex],
                                 color=next(plotOptions["colorCycle"]))
    return axisObj
