import argparse
import numpy

imageAP = argparse.ArgumentParser("Plots the image loaded as dataset to a given axis coordinate dimension.")
imageAP.add_argument("imageDataset", help="Name of the dataset containing the RGB(A) data. They should be in an unrolled loop.")
imageAP.add_argument("imageRect", nargs=4, type=float, help="Rectangle for the image to be drawn into, in axes coordinates. (x,y,width,height).")
imageAP.add_argument("--shape", type=int, nargs=2, help="Shape of the image, in format width,height.")

def command(axes, datasets, argString):
    args = imageAP.parse_args(argString)
    numberOfChannels = len(datasets[args.imageDataset])
    # Shape the image
    shapedImage = numpy.array(datasets[args.imageDataset]).reshape([numberOfChannels] + args.shape)
    # Transform to correct shape for plotting
    shapedImage = numpy.moveaxis(shapedImage, 0, -1)
    # Plot the image, with transformation of the coordinates
    axes.imshow(shapedImage, transform=axes.transAxes, aspect="auto", origin="lower", extent=(args.imageRect[0],args.imageRect[0]+args.imageRect[2],args.imageRect[1],args.imageRect[1]+args.imageRect[3]))
    return axes, datasets
