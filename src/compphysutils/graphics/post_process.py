import argparse

def gapRead(datagroups, args):
    # Prepared for reading of gap - expects datagrous [energy, occupation]
    LUMO = 0
    HOMO = 0
    for i in range(len(datagroups[0])):
        # Data are ordered by energy
        if datagroups[1][i] == 0:
            LUMO = datagroups[0][i]
            HOMO = datagroups[0][i-1]
            break
    return [[LUMO - HOMO]]

levelsGetAP = argparse.ArgumentParser()
levelsGetAP.add_argument("--above", default=True, action="store_true", help="Scan for the given number of levels above HOMO.")
levelsGetAP.add_argument("--below", default=False, action="store_true", help="Scan for the given number of levels below and including HOMO.")
levelsGetAP.add_argument("levelNum", default=3, type=int, help="Number of levels to scan for.")
def levelsGet(dataset, argsList):
    # This is just a helper function that is used in specific commands
    args = levelsGetAP.parse_args(argsList)
    levels= []
    for i in range(args.levelNum):
        levels.append(0.0)
    if args.below:
        homoIndex = 0
        for i in range(len(dataset[0])):
            # Scan for HOMO
            if dataset[1][i] == 0:
                homoIndex = i-1
                break
        for i in range(args.levelNum):
            levels[i] = dataset[O][homoIndex - args.levelNum + i + 1]
    else:
        # Assume above
        lumoIndex = 0
        for i in range(len(dataset[0])):
            # Scan for LUMO
            if dataset[1][i] == 0:
                lumoIndex = i
                break
        for i in range(args.levelNum):
            levels[i] = dataset[0][lumoIndex + i]
    return [levels]

def levelsSpacingAverage(dataset, argsList):
    levels = levelsGet(dataset, argsList)
    sumLin = 0
    sumSq = 0
    for i in range(len(levels[0])-1):
        sumLin += levels[0][i+1] - levels[0][i]
        sumSq += (levels[0][i+1] - levels[0][i]) ** 2
    mean = sumLin / len(levels[0])
    # We know the whole population of the levels
    stddev = ((sumSq / len(levels[0])) - (mean ** 2)) ** 0.5
    return [[mean],[stddev]]


postProcessCommands = {
    "gap" : gapRead,
    "levels" : levelsGet,
    "level-spacing" : levelsSpacingAverage
}
