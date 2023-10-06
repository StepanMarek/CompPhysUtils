import argparse
import numpy

difAP = argparse.ArgumentParser()
difAP.add_argument("new_name", help="Name of the dataset where the sum will be saved.")
difAP.add_argument("coords", nargs="+", help="Dataset name and column number pairs for source columns.")

def command(datasets, argString):
    args = difAP.parse_args(argString)
    if len(args.coords) % 2 != 0:
        raise ValueError("Wrong number of column coords - need name and column index for each column.")
    # Determine the columns
    matrix = []
    for i in range(0,len(args.coords), 2):
        matrix.append(datasets[args.coords[i]][int(args.coords[i+1])])
    matrix = numpy.array(matrix)
    summation = list(numpy.sum(matrix, axis=0))
    datasets[args.new_name] = [summation]
    return datasets
