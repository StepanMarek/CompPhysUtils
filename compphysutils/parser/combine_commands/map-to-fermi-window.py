import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--bias", default=0.0, type=float, help="Bias (in V) around the Fermi energy to use for the construction of Fermi window. Default : 0.0 - near equilibrium")
ap.add_argument("--biasCenter", default="middle", help="On which electrode to apply the bias. Default : middle - apply bias symmetrically.")
ap.add_argument("--fermi", default=0.0, type=float, help="Fermi energy (in eV). Default : 0 - assumes energies relative to Fermi energy")
ap.add_argument("--temp", default=10.0, type=float, help="Temperature (in Kelvin). Default 10.0")
ap.add_argument("--phiTolerance", default=30.0, type=float, help="Maximum value of the exponent in fermi distribution, where the distribution is not assumed to be strictly 1 or 0. Default : 30.0 - strong")
ap.add_argument("--unit", default="eV", help="Energy units to use for input energy. Default : eV")
ap.add_argument("newSet", help="Name of the new dataset")
ap.add_argument("colCoords", nargs="+", help="Pairs of column coordinates, which represent the columns onto which the Fermi window function should be mapped.")

def fermiDist(E, shift, beta, phiTolerance):
    phi = (E - shift) * beta
    if phi > phiTolerance:
        return 0
    elif phi < -phiTolerance:
        return 1
    else:
        return 1/(1+np.exp(phi))

def fermiWindow(E, shift, beta, biasL, biasR, phiTolerance):
    return fermiDist(E, shift + biasL, beta, phiTolerance) - fermiDist(E, shift + biasR, beta, phiTolerance)

def command(datasets, argString):
    args = ap.parse_args(argString)
    # Sanity check
    if len(args.colCoords) % 2 != 0:
        raise ValueError("Column coordinates need to come in pairs.")
    datasets[args.newSet] = []
    # Inverse temperature, in eV^{-1}
    # https://physics.nist.gov/cgi-bin/cuu/Value?kev
    beta = 1/(8.617333262e-5 * args.temp)
    multiplier = 1.0
    # For Hartree units, multiply energy by hartree energy
    if args.unit == "H":
        # https://physics.nist.gov/cgi-bin/cuu/Value?hrev
        multiplier = 27.211386245988
    biasL = args.bias / 2
    biasR = - args.bias / 2
    if args.biasCenter == "left":
        biasL = args.bias
        biasR = 0
    elif args.biasCenter == "right":
        biasL = 0
        biasR = args.bias
    for i in range(0, len(args.colCoords), 2):
        datasets[args.newSet].append(list(map(lambda x: fermiWindow(x * multiplier, args.fermi, beta, biasL, biasR, args.phiTolerance), datasets[args.colCoords[0]][int(args.colCoords[1])])))
    return datasets
