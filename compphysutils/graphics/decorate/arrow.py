import argparse

AP = argparse.ArgumentParser()
AP.add_argument("--start", nargs=2, type=float, default=[0.0,0.0], help="Data coordinates of the arrow base.")
AP.add_argument("--end", nargs=2, type=float, default=[0.0,0.0], help="Data coordinates of the arrow head.")
AP.add_argument("--transform", default="data", choices=["data", "axes"], help="Transformation to use - default is data, can also use axes.")
AP.add_argument("--width", default=1.0, type=float, help="Width of the arrow.")
AP.add_argument("--color", default="k", help="Color of the arrow.")

def command(axes, datasets, argString):
    args = AP.parse_args(argString)

    # Map Matplotlib shorthand colors to TikZ/LaTeX colors
    color_map = {
        "k": "black",
        "r": "red",
        "b": "blue",
        "g": "green",
        "y": "yellow",
        "m": "magenta",
        "c": "cyan",
        "w": "white"
    }
    color = color_map.get(args.color, args.color)

    # Draw arrow
    axes.arrow(
        start=args.start,
        end=args.end,
        color=color,
        width=args.width,
        transform=args.transform
    )

    return axes, datasets
