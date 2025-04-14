import argparse
import numpy

ap = argparse.ArgumentParser(description="Expects dataset with ND Vector field - N coordinates + N vector components in columns, in unrolled loops.")
ap.add_argument("--constantIndex", default=-1, type=int, help="Index of the remaining coordinate, which is kept constant. Special value -1 is used for signaling that all axes should be kept.")
ap.add_argument("--planeIndex", default=0, type=int, help="Position of the plane along the constant index, i.e. whether to take the plane at x = 10 or x = 20 etc.")
ap.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Whether to output additional information to stdout.")
ap.add_argument("--boxSize", help="Defines the gridsize, e.g. 20,20,20, from outer-most (slowest changing) to inner most coordinate", type=lambda x: list(map(int, x.split(","))))
ap.add_argument("--normalize", action="store_true", help="Normalizes the vectors pointwise - creating direction only arrows.")
ap.add_argument("--axisCompMap", help="Defines map between loop axes (indexed from outer-most to inner-most) and column positions. Comma separated indices of columns for each dimension.", type=lambda x: list(map(int, x.split(","))))
ap.add_argument("--angles", default="xy", help="Angles setting of quiver matlab primitive. Default : xy - angles are determined by adding components to position vector.")
ap.add_argument("--scale", default=1, type=float, help="Scale used for the matlab primitive. Default : 1")
ap.add_argument("--scaleUnits", default="xy", help="Scale units used for the matlab primitive. Default : xy")
ap.add_argument("--units", default="xy", help="Units used for the matlab primitive. Default : xy")
ap.add_argument("--pivot", default="tail", help="Pivot used for the matlab primitive. Default : tail")
ap.add_argument("--headlength", default=10, type=float, help="Headlength argument passed to the matlab primitive. Default : 10")
ap.add_argument("--headwidth", default=10, type=float, help="Headlength argument passed to the matlab primitive. Default : 10")
ap.add_argument("--headaxislength", default=10, type=float, help="Headlength argument passed to the matlab primitive. Default : 10")
ap.add_argument("--stride", default=1, type=int, help="Optionally, stride the points in both directions to reduce the number of points.")

def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    args = ap.parse_args(plotOptions["plotArgString"])
    # Check labels
    if not datasetLabels:
        datasetLabels = [False] * len(datasets)
    for datasetIndex in range(len(datasets)):
        # Check dimensionality
        dimensions = len(datasets[datasetIndex]) // 2
        # Ignore extra columns beyond the expected dimensions TODO : Change this/warn user?
        # Shape the fields
        coordinates = numpy.array(datasets[datasetIndex][0:dimensions]).reshape((dimensions, *args.boxSize))
        components = numpy.array(datasets[datasetIndex][dimensions:2*dimensions]).reshape((dimensions, *args.boxSize))
        # Move the constant axis 
        if args.constantIndex != -1:
            coordinates = numpy.moveaxis(coordinates, args.constantIndex+1, 1)[:,args.planeIndex]
            components = numpy.moveaxis(components, args.constantIndex+1, 1)[:,args.planeIndex]
            if args.verbose:
                # Output value of the coordinate
                print("quiver : keeping coordinate "+str(args.constantIndex)+"->"+str(args.axisCompMap[args.constantIndex])+" constant at "+str(coordinates[args.axisCompMap[args.constantIndex]].flatten()[0]))
            # Delete the constant axis components
            coordinates = numpy.delete(coordinates, args.axisCompMap[args.constantIndex], axis=0)
            components = numpy.delete(components, args.axisCompMap[args.constantIndex], axis=0)
        # With these ready, output vectors
        if args.normalize:
            components = components / (numpy.sum(components ** 2, axis=0) ** 0.5)
        # Change default arrow style to resamble annotation arrows
        if args.stride != 1:
            print(coordinates.shape)
            coordinates = numpy.lib.stride_tricks.as_strided(coordinates,
                    shape=(coordinates.shape[0], coordinates.shape[1]//args.stride, coordinates.shape[2]//args.stride),
                    strides=(coordinates.strides[0], coordinates.strides[1]*args.stride, coordinates.strides[2]*args.stride))
            print(coordinates.shape)
            components = numpy.lib.stride_tricks.as_strided(components,
                    shape=(components.shape[0], components.shape[1]//args.stride, components.shape[2]//args.stride),
                    strides=(components.strides[0], components.strides[1]*args.stride, components.strides[2]*args.stride))
        axisObj.quiver(*coordinates, *components,
            label=datasetLabels[datasetIndex],
            color=next(plotOptions["colorCycle"]),
            angles=args.angles,
            scale=args.scale,
            scale_units=args.scaleUnits,
            units=args.units,
            pivot=args.pivot,
            headlength=args.headlength,
            headaxislength=args.headaxislength,
            headwidth=args.headwidth
        )
    return axisObj
