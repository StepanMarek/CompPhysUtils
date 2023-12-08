import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--unit", default="A", help="Unit of distance to be set in the dataset - default is Angström (different from the units used, which are H).")

argDefaults = ""

bohrToAngstrom = 0.529177210903

def line(textline, unit="A"):
    # Only care about the non commented lines
    if textline[0] == "$":
        return False
    fields = textline.split()
    if unit == "A":
        multiplier = bohrToAngstrom
    else:
        multiplier = 1
    for i in range(3):
        fields[i] = float(fields[i])*multiplier
    # Only output element name, do not output fixed letter
    return fields[0:4]

def initParserObjects(parserArgs):
    args = ap.parse_args(parserArgs)
    return args.unit

def writeLine(datarow):
    # Writes the line in a given format
    doubleFormat = " >-20.14f"
    coords = (("{:"+doubleFormat+"}")*3).format(*map(lambda x: x / bohrToAngstrom, datarow[0:3]))
    return (coords + "{: >8}".format(datarow[3].lower()))

def writeHeaders(dataset):
    return "$coord"

def writeFooters(dataset):
    return "$user-defined bonds\n$end"
