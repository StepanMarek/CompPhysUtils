import argparse
import numpy
from ..parser import parse_ranges, ranges_to_indices

ap = argparse.ArgumentParser(prog="plane-rotate", description="Rotate the subset of atoms by an angle in plane. The plane is defined by the center (average) of the atom positions and two specified atoms.")
ap.add_argument("--rowRange", type=parse_ranges, default=":", help="Range of row indices that define the atoms for which the average plane is to be determined.")
ap.add_argument("angle", type=float, default=0.0, help="Angle of rotation, in degrees.")

def command(dataset, argString):
    args = ap.parse_args(argString)
    rotAngle = args.angle * numpy.pi / 180
    # Start by converting chosen points to vectors in numpy
    points = []
    rows = ranges_to_indices(args.rowRange, dataset[0])
    for i in rows:
        points.append([])
        for j in range(3):
            points[-1].append(dataset[j][i])
    points = numpy.array(points)
    # Get the center of mass
    rcm = numpy.average(points, axis=0)
    # Transform points to rcm
    points = points - rcm
    # Get the initial normal vector guess
    # Will do index 0 vector products only - (N-1) relevant vectors
    # Generate vectors
    normalVectors = numpy.cross(points[0], points[1:])
    # Now, check whether projection is possitive - if it is not, invert
    # Do via masking
    projections = numpy.dot(normalVectors, numpy.cross(points[0], points[1]))
    # mask
    projections = projections > 0
    # shift
    projections = projections * 2 - 1
    # apply mask
    normalVectors[:,0] = projections * normalVectors[:,0]
    normalVectors[:,1] = projections * normalVectors[:,1]
    normalVectors[:,2] = projections * normalVectors[:,2]
    # Average the vectors to get average normal vector
    averageNormalVector = numpy.average(normalVectors, axis=0)
    # Normalize
    averageNormalVector = averageNormalVector / numpy.linalg.norm(averageNormalVector)
    # Now, for each vector, get :
    # - component along the normal vector normComp
    # - component tangent to plane 1 tangCompOne
    # - component tanget to plane and perpendicular to tangCompOne, tangCompTwo, obtained by cross-product
    normComp = numpy.full(points.shape, averageNormalVector)
    normProjections = numpy.dot(points, averageNormalVector)
    normComp[:,0] = normProjections * normComp[:,0]
    normComp[:,1] = normProjections * normComp[:,1]
    normComp[:,2] = normProjections * normComp[:,2]
    tangCompOne = points - normComp
    tangCompTwo = numpy.cross(averageNormalVector, points)
    # Combine these to rotated points
    rotatedPoints = numpy.sin(rotAngle) * tangCompTwo + numpy.cos(rotAngle) * tangCompOne + normComp
    # Reset the pivot
    rotatedPoints = rotatedPoints + rcm
    # Prepend and append 
    newDataset = [[],[],[],[]]
    rotated_index = 0
    for j in range(len(dataset[0])):
        for i in range(3):
            if j in rows:
                # Take values from rotatedPoints
                newDataset[i].append(rotatedPoints[rotated_index][i])
            else:
                # Take values from original dataset
                newDataset[i].append(dataset[i][j])
        if j in rows:
            rotated_index += 1
        # Copy name of element
        newDataset[3].append(dataset[3][j])
    return newDataset
