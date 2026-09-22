import argparse

AP = argparse.ArgumentParser()
AP.add_argument("--coords", nargs=2, type=float, default=[0.0,0.0], help="Data coordinates of the text.")
AP.add_argument("--axes", action="store_true", help="Instead of data coordinates, use axes coordinates.")
AP.add_argument("text", nargs="*", help="Text to be added at given coordinates.")

def command(axes, datasets, argString):
    args = AP.parse_args(argString)
    transform = "data"
    if args.axes:
        transform = "axes"
    # Draw the text
    axes.text(args.coords, " ".join(args.text), transform=transform)
    return axes, datasets
