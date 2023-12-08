import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument("--temp", type=float, default=77, help="Temperature (in K) to average with.")
ap.add_argument("--unit", default="eV", help="Energy unit used [default : eV]")
ap.add_argument("new_name", help="Name of the new dataset where the average results will be located.")
ap.add_argument("energy_coords", nargs=2, help="Dataset name and column number of the energies to be associated with the values to be averaged. THe number of values must be the same as the number of datasets for averaging.")
ap.add_argument("data_coords", nargs="+", help="Dataset name and column number of the set of variables to be averaged.")

def command(datasets, argString):
    args = ap.parse_args(argString)
    # https://physics.nist.gov/cgi-bin/cuu/Value?kev
    beta = 1/(8.617333262e-5 * args.temp)
    # If using hartree units instead of eV, change units
    if args.unit == "H":
        beta = beta/(3.6749322175655e-2)
    # Check the correctness of dimensions
    energies = datasets[args.energy_coords[0]][int(args.energy_coords[1])]
    N = len(energies)
    if N != (len(args.data_coords) / 2):
        raise IndexError("Need to have the same number of datagroups to average as averaging energies.")
    # Proceed
    # Start by finding the baseline energy
    baseline = min(energies)
    # Prepare partition function
    partf = 0
    boltzfact = 1
    # Prepare new data, first datagroup determines the number of averaged values
    new_data = []
    M = len(datasets[args.data_coords[0]][int(args.data_coords[1])])
    for j in range(M):
        new_data.append(0)
    for i in range(N):
        # Determine energy difference
        dE = energies[i] - baseline
        # Determine boltzmann factor
        boltzfact = math.exp(- beta * dE)
        # Update partition function
        partf += boltzfact
        # Now, for each value in the relevant dataset, add the Boltzmann weighted value to new data
        for j in range(M):
            new_data[j] += boltzfact * datasets[args.data_coords[2*i]][int(args.data_coords[2*i+1])][j]
    # Now, each element of new_data contains Boltzmann sum, need to divide each element by the partition function
    for j in range(M):
        new_data[j] = new_data[j] / partf
    # Finally, update and return the datasets
    datasets[args.new_name] = [new_data]
    return datasets
