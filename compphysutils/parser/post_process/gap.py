import argparse

gapReadAP = argparse.ArgumentParser(prog="gap", description="Calculates the gap between occupied and unoccupied states, or any other indicator that crosses from 2 to 0 at the boundary.")
gapReadAP.add_argument("--fractional", default=False, action="store_true", help="Instead of integer occupation, assume fractional occupation is present, and set LUMO to first level, where occupation is less than one electron.")
gapReadAP.add_argument("--energy_col", "-e", dest="energy_col", type=int, default=0, help="Coordinates of the energy column. [default : 0]")
gapReadAP.add_argument("--occ_col", "-n", dest="occ_col", type=int, default=1, help="Coordinates of the occupation column. [default : 1]")

def command(datagroups, argList):
    # Prepared for reading of gap - expects datagrous [energy, occupation]
    LUMO = 0
    HOMO = 0
    args = gapReadAP.parse_args(argList)
    for i in range(len(datagroups[args.energy_col])):
        # Data are ordered by energy
        if not args.fractional:
            if datagroups[args.occ_col][i] == 0:
                LUMO = datagroups[args.energy_col][i]
                HOMO = datagroups[args.energy_col][i-1]
                break
        else:
            if datagroups[args.occ_col][i] < 1.0:
                LUMO = datagroups[args.energy_col][i]
                HOMO = datagroups[args.energy_col][i-1]
                break
    return [[LUMO - HOMO]]
