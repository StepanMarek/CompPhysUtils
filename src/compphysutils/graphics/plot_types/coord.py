import argparse
import numpy
import matplotlib.tri as mtri

ap = argparse.ArgumentParser(description="Simple render of the atomic coordinates from a coord dataset.")

ap.add_argument("--view", type=lambda x: list(map(float, x.split(","))), help="Camera position in angular coordinates in degrees (azimuthal,elevation,roll). Default : (0,0,0)", default=[0,0,0])

colors = {
    "au" : "#ffcc00",
    "na" : "#ffff00",
    "fe" : "#ff9933",
    "h"  : "#ffffff",
    "c"  : "#111111",
    "o"  : "#ff0000",
    "n"  : "#0000ff",
    "s"  : "#ffeb00",
    "mo" : "#006792"
}

radii = {
    "au" : 1.5,
    "na" : 1.2,
    "fe" : 1.4,
    "h"  : 0.5,
    "c"  : 1.0,
    "o"  : 1.1,
    "n"  : 1.1,
    "s"  : 1.3,
    "mo" : 1.3,
}

def plotSpheres(axes3d, position=numpy.array([[0.0],[0.0],[0.0]]), elements=False):
    # Create the mesh
    phi = numpy.linspace(0, numpy.pi*2, 20)
    theta = numpy.linspace(0, numpy.pi, 20)
    theta, phi = numpy.meshgrid(theta, phi)
    phi, theta = phi.flatten(), theta.flatten()
    x0 = numpy.cos(phi) * numpy.sin(theta)
    y0 = numpy.sin(phi) * numpy.sin(theta)
    z0 = numpy.cos(theta)
    # Add triangulation
    tri = mtri.Triangulation(theta, phi)
    for j in range(len(position[0])):
        if not elements:
            x = x0 - position[0,j]
            y = y0 - position[1,j]
            z = z0 - position[2,j]
            axes3d.plot_trisurf(x, y, z, triangles=tri.triangles, edgecolor="none",linewidth=0,antialiased=False,color="b")
        else:
            try:
                x = radii[elements[j].lower()] * x0 - position[0,j]
                y = radii[elements[j].lower()] * y0 - position[1,j]
                z = radii[elements[j].lower()] * z0 - position[2,j]
            except KeyError:
                x = x0 - position[0,j]
                y = y0 - position[1,j]
                z = z0 - position[2,j]
            try:
                axes3d.plot_trisurf(x, y, z, triangles=tri.triangles, edgecolor="none",linewidth=0,antialiased=False,color=colors[elements[j].lower()])
            except KeyError:
                axes3d.plot_trisurf(x, y, z, triangles=tri.triangles, edgecolor="none",linewidth=0,antialiased=False,color="b")


def plot(datasets, axisObj, **plotOptions):
    figure = plotOptions["figure"]
    figure.clf()
    axes = figure.add_axes((0.0,0.0,1.0,1.0),projection="3d")
    axes.set_axis_off()
    args = ap.parse_args(plotOptions["plotArgString"])
    for i in range(len(datasets)):
        #axes.scatter(datasets[i][0], datasets[i][1], datasets[i][2])
        if len(datasets[i]) > 3:
            plotSpheres(axes, position=numpy.array(datasets[i][0:3]), elements=datasets[i][3])
        else:
            plotSpheres(axes, position=numpy.array(datasets[i][0:3]))
    axes.view_init(elev=args.view[1], azim=args.view[0], roll=args.view[2])
    return axes
