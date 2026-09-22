import argparse
import numpy
from matplotlib import colors as mplc

ap = argparse.ArgumentParser()
ap.add_argument("--boxSize", type=lambda x:list(map(int, x.split(","))), help="Shape of the data (2D), order as xy")
ap.add_argument("--cmap", default="Reds", help="Used colormap")
ap.add_argument("--norm", default="lin", choices=["lin", "log"], help="Normalisation of the data to range [0,1], can be lin, log.")
ap.add_argument("--vmin", default=False, type=float, help="Minimum value used for the colormap normalisation. Default : minimum of value range")
ap.add_argument("--vmax", default=False, type=float, help="Maximum value used for the colormap normalisation. Default : maximum of value range")
ap.add_argument("--noBar", action="store_true", help="Do not show the colorbar [default : show the colorbar]")
ap.add_argument("--barXpos", default=0.0, type=float, help="Horizontal (x) offset of the colorbar. [default : 0.0]")
ap.add_argument("--barYpos", default=0.5, type=float, help="Horizontal (x) offset of the colorbar. [default : 0.5]")
#
#normMap = {
#    "lin" : mplc.Normalize,
#    "log" : mplc.LogNorm
#}

def plot(datasets, axisObj, datasetLabels=False, figure=False, **plotOptions):
    """
    Plots 2D colormap with added colorbar mapping from maximum to minimum
    """
    if not datasetLabels:
        datasetLabels = [False] * len(datasets)
    args = ap.parse_args(plotOptions["plotArgString"])
    # Iterate over datasets
    for datasetIndex in range(len(datasets)):
        # Shape the data
        x = datasets[datasetIndex][0]
        y = datasets[datasetIndex][1]
        vals = datasets[datasetIndex][2]
        # Start according to default loop order
        x = numpy.array(x).reshape(args.boxSize)
        y = numpy.array(y).reshape(args.boxSize)
        vals = numpy.array(vals).reshape(args.boxSize)
        # But, we need x-axis outer always
        #if args.boxOrder[0] == "y":
        #    x = x.transpose()
        #    y = y.transpose()
        #    vals = vals.transpose()
        ## Find minima and maxima
        vmin = numpy.min(vals)
        if args.vmin:
            vmin = args.vmin
        vmax = numpy.max(vals)
        if args.vmax:
            vmax = args.vmax
        # Plot data
        # TODO : range (vmin,vmax), cmap
        # TODO : mpl used , shading="nearest"
        axImage = axisObj.colormap(x, y, vals, cmap=args.cmap, norm=args.norm, vmin=vmin, vmax=vmax)
        # TODO : Colorbar
        ## Append color bar
        #if not args.noBar:
        #    figure.colorbar(axImage, ax=axisObj, anchor=(args.barXpos, args.barYpos))
    return axisObj
