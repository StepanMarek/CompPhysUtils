import argparse
import matplotlib

AP = argparse.ArgumentParser()
AP.add_argument("--start", nargs=2, type=float, default=[0.0,0.0], help="Data coordinates of the rectangle start.")
AP.add_argument("--end", nargs=2, type=float, default=[0.0,0.0], help="Data coordinates of the rectangle end.")
AP.add_argument("--transform", default=False, help="Transformation to use - default is data, can also use axes.")
AP.add_argument("--borderwidth", default=0.01, help="Width of the border")
AP.add_argument("--bordercolor", default="k", help="Color of the border.")
AP.add_argument("--linestyle", default="-", help="Linestyle of the border.")

def command(axes, datasets, argString):
    args = AP.parse_args(argString)
    # Draw the text
    dxdy = [args.end[0] - args.start[0], args.end[1] - args.start[1]]
    if args.transform == "axes":
        axes.add_patch(matplotlib.patches.Rectangle(args.start, *dxdy, lw=args.borderwidth, color=args.bordercolor, fill=False, linestyle=args.linestyle, transform=axes.transAxes))
    else:
        axes.add_patch(matplotlib.patches.Rectangle(args.start, *dxdy, lw=args.borderwidth, color=args.bordercolor, fill=False, linestyle=args.linestyle))
    return axes, datasets
