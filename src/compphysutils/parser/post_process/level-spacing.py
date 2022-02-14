from .levels import command as levelsGet

def command(dataset, argsList):
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
