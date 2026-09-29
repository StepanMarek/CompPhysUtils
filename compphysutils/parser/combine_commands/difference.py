import argparse

difAP = argparse.ArgumentParser()
difAP.add_argument("--abs", action="store_true", default=False, help="Whether to take absolute value of the difference instead of signed value. [default : False]")
difAP.add_argument("new_name", help="Name of the dataset where the difference will be saved.")
difAP.add_argument("positive_coords", nargs=2, help="Dataset name and column number of first datagroup, taken positively in the difference.")
difAP.add_argument("negative_coords", nargs=2, help="Dataset name and column number of the second datagroup, taken negatively in the difference.")

def command(datasets, argString):
    args = difAP.parse_args(argString)
    # Determine the columns
    pos = datasets[args.positive_coords[0]][int(args.positive_coords[1])]
    neg = datasets[args.negative_coords[0]][int(args.negative_coords[1])]
    dif = []
    for i in range(len(pos)):
        dif.append(pos[i] - neg[i])
    if args.abs:
        dif = list(map(abs, dif))
    datasets[args.new_name] = [dif]
    return datasets
