import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--boxSize", type=lambda x: list(map(int, x.split(","))), help="Size of the unrolled loop, starting from the outer-most axis.")
ap.add_argument("--axisIndex", type=int, help="Index of the axis to be rolled - starting from 0 for the outer-most loop.")
ap.add_argument("newSet", help="New dataset where to store the rolled axis.")
ap.add_argument("colCoords", nargs=2, help="Column coordinates of the unrolled loop")

def command(datasets, argString):
    args = ap.parse_args(argString)
    # First, shape the array
    arrShaped = np.array(datasets[args.colCoords[0]][int(args.colCoords[1])]).reshape(args.boxSize)
    # Now, move the required axis to inner-most axis
    arrShaped = np.moveaxis(arrShaped, args.axisIndex, -1)
    # Now, sequentially move to the inner-most axis, which contains the required object
    for i in range(len(args.boxSize)-1):
        arrShaped = arrShaped[0,...]
    # Now, output the rolled axis
    datasets[args.newSet] = [arrShaped]
    return datasets
