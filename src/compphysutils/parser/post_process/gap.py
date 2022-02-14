import argparse

gapReadAP = argparse.ArgumentParser()
gapReadAP.add_argument("--fractional", default=False, action="store_true", help="Instead of integer occupation, assume fractional occupation is present, and set LUMO to first level, where occupation is less than one electron.")
def command(datagroups, argList):
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
    return [[LUMO - HOMO]]
