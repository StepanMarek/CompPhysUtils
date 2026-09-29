import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--unit", default="A", help="Unit of distance to be set in the dataset - default is Angström.")

argDefaults = ""

bohrToAngstrom = 0.529177210903

def line(textline, unit="A"):
    # Only read lines starting with keyword atom
    if textline[0:4] != "atom":
        return False
    fields = textline.split()
    if unit == "A":
        multiplier = 1
    else:
        multiplier = 1/bohrToAngstrom
    for i in range(1,4):
        fields[i] = float(fields[i])*multiplier
    return fields[1:]

def initParserObjects(parserArgs):
    args = ap.parse_args(parserArgs)
    return args.unit

def writeLine(datarow):
    doubleFormat = " >-20.14f"
    elemName = datarow[3][0].upper()
    if len(datarow[3][0]) > 0:
        elemName = elemName + datarow[3][1:]
    return "atom "+(("{:"+doubleFormat+"}")*3).format(*datarow[0:3])+" "+elemName
