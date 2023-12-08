def command(datagroups, argString):
    newGroups = []
    for i in range(len(datagroups)):
        newGroups.append([sum(datagroups[i]) / len(datagroups[i])])
    return newGroups
