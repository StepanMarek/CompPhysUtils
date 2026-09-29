import argparse

levelsGetAP = argparse.ArgumentParser()
levelsGetAP.add_argument("--above", default=True, action="store_true", help="Scan for the given number of levels above HOMO.")
levelsGetAP.add_argument("--below", default=False, action="store_true", help="Scan for the given number of levels below and including HOMO.")
levelsGetAP.add_argument("--fractional", default=False, action="store_true", help="Instead of integer occupation, set LUMO to first level where occupation is less than one.")
levelsGetAP.add_argument("--homo_align", default=False, action="store_true", help="Set HOMO level to 0, offseting the other energy levels accordingly.")
levelsGetAP.add_argument("levelNum", default=3, type=int, help="Number of levels to scan for.")
def command(dataset, argsList):
    # This is just a helper function that is used in specific commands
    args = levelsGetAP.parse_args(argsList)
    levels= []
    for i in range(args.levelNum):
        levels.append(0.0)
    if args.below:
        homoIndex = 0
        for i in range(len(dataset[0])):
            # Scan for HOMO
            if dataset[1][i] == 0 or (dataset[1][i] < 1.0 and args.fractional):
                homoIndex = i-1
                break
        for i in range(args.levelNum):
            levels[i] = dataset[0][homoIndex - args.levelNum + i + 1]
        if args.homo_align:
            for i in range(len(levels)):
                levels[i] = levels[i] - dataset[0][homoIndex]
    else:
        # Assume above
        lumoIndex = 0
        for i in range(len(dataset[0])):
            # Scan for LUMO
            if dataset[1][i] == 0 or (dataset[1][i] < 1.0 and args.fractional):
                lumoIndex = i
                break
        for i in range(args.levelNum):
            levels[i] = dataset[0][lumoIndex + i]
        if args.homo_align:
            for i in range(len(levels)):
                levels[i] = levels[i] - dataset[0][lumoIndex - 1]
    return [levels]
