import argparse
import matplotlib

AP = argparse.ArgumentParser()
AP.add_argument("--start", nargs=2, type=float, default=[0.0,0.0], help="Data coordinates of the arrow base.")
AP.add_argument("--end", nargs=2, type=float, default=[0.0,0.0], help="Data coordinates of the arrow head.")
AP.add_argument("--transform", default=False, help="Transformation to use - default is data, can also use axes.")
AP.add_argument("--width", default=0.01, type=float, help="Width of the arrow.")
AP.add_argument("--color", default="k", help="Color of the arrow.")
AP.add_argument("--arrowstyle", default=False, help="Linestyle of the arrow.")
AP.add_argument("--connectionstyle", default="arc3", help="Connection style argument for the arrow.")

def command(axes, datasets, argString):
    args = AP.parse_args(argString)
    arrowprops = {}
    arrowprops["color"] = args.color
    arrowprops["connectionstyle"] = args.connectionstyle
    if not args.arrowstyle:
        # Default is similar to default quiver style
        arrowprops["arrowstyle"] = matplotlib.patches.ArrowStyle.Simple(head_length=1.0, tail_width=0.2, head_width=0.6)
    if args.transform == "axes":
        axes.annotate("", args.end, args.start, xycoords="axes fraction", arrowprops=arrowprops)
    else:
        axes.annotate("", args.end, args.start, xycoords="data", arrowprops=arrowprops)
    return axes, datasets
