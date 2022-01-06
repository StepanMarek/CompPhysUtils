def gapRead(datagroups, *args):
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

postProcessCommands = {
    "gap" : gapRead
}
