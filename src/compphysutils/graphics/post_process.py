import argparse

gapReadAP = argparse.ArgumentParser()
gapReadAP.add_argument("--fractional", default=False, action="store_true", help="Instead of integer occupation, assume fractional occupation is present, and set LUMO to first level, where occupation is less than one electron.")
def gapRead(datagroups, argList):
    # Prepared for reading of gap - expects datagrous [energy, occupation]
    LUMO = 0
    HOMO = 0
    args = gapReadAP.parse_args(argList)
    for i in range(len(datagroups[0])):
        # Data are ordered by energy
        if not args.fractional:
            if datagroups[1][i] == 0:
                LUMO = datagroups[0][i]
                HOMO = datagroups[0][i-1]
                break
        else:
            if datagroups[1][i] < 1.0:
                LUMO = datagroups[0][i]
                HOMO = datagroups[0][i-1]
                break
    print(LUMO, HOMO, LUMO-HOMO)
    return [[LUMO - HOMO]]

levelsGetAP = argparse.ArgumentParser()
levelsGetAP.add_argument("--above", default=True, action="store_true", help="Scan for the given number of levels above HOMO.")
levelsGetAP.add_argument("--below", default=False, action="store_true", help="Scan for the given number of levels below and including HOMO.")
levelsGetAP.add_argument("--fractional", default=False, action="store_true", help="Instead of integer occupation, set LUMO to first level where occupation is less than one.")
levelsGetAP.add_argument("--homo_align", default=False, action="store_true", help="Set HOMO level to 0, offseting the other energy levels accordingly.")
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

def levelsSpacingAverage(dataset, argsList):
    levels = levelsGet(dataset, argsList)
    sumLin = 0
    sumSq = 0
    for i in range(len(levels[0])-1):
        sumLin += levels[0][i+1] - levels[0][i]
        sumSq += (levels[0][i+1] - levels[0][i]) ** 2
    mean = sumLin / (len(levels[0])-1)
    # We know the whole population of the levels
    stddev = ((sumSq / (len(levels[0])-1)) - (mean ** 2)) ** 0.5
    return [[mean],[stddev]]


postProcessCommands = {
    "gap" : gapRead,
    "levels" : levelsGet,
    "level-spacing" : levelsSpacingAverage
}
