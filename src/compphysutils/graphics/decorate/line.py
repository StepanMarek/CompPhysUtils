import argparse

lineAP = argparse.ArgumentParser()
lineAP.add_argument("--vert", action="store_true", default=False, help="Draw vertical line instead of horizontal line.")
# Instead of parsing the kwargs straight, do argument conversion - is more backend agnostic
lineAP.add_argument("--color", default="k", help="Color of the line. [default : k = black]")
lineAP.add_argument("--style", default="-", help="Style of the line. [default : - = solid]")
lineAP.add_argument("coord", type=float, default=0.0, help="Coordinate of the line to be drawn [default : data coordinates]")
# TODO : Transforms to other coordinate types

def command(axes, datasets, argString):
    args = lineAP.parse_args(argString)
    # Draw a line
    if args.vert:
        axes.axvline(args.coord, ls=args.style, c=args.color)
    else:
        axes.axhline(args.coord, ls=args.style, c=args.color)
    return axes, datasets
