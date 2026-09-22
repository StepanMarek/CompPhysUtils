import argparse
import matplotlib.image
import numpy as np

def initParserObjects(parserArgs):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", action="store_true", help="Whether to output debug information. Default : False")
    args = ap.parse_args(parserArgs)
    return [args]

def file(filename, args):
    image = np.array(matplotlib.image.imread(filename))
    # Output dimension data in verbose
    if args.v:
        print("Image box size : ({:d},{:d})".format(image.shape[0], image.shape[1]))
    # Flatten image channels
    flatImage = []
    for i in range(image.shape[2]):
        flatImage.append(image[:,:,i].flatten())
    return flatImage
