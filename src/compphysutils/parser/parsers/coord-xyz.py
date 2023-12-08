import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--unit", default="A", help="Unit of distance to be set in the dataset - default is Angström (different from the units used, which are H).")

argDefaults = ""

bohrToAngstrom = 0.529177210903

def line(textline, numLines, unit="A"):
    currLine = numLines["numLines"]
    if currLine < 2:
        # Skip the initial information only lines
        numLines["numLines"] += 1
        return False
    fields = textline.split()
    if unit == "H":
        multiplier = 1/bohrToAngstrom
    else:
        multiplier = 1
    for i in range(1,4):
        fields[i] = float(fields[i])*multiplier
    return fields[1:] + fields[0:1]

def initParserObjects(parserArgs):
    args = ap.parse_args(parserArgs)
    return {"numLines" : 0}, args.unit

def writeLine(datarow):
    # Assumes standard format for coord data
    return " ".join([datarow[3].upper()] + list(map(str,datarow[0:3])))

def writeHeaders(dataset):
    return str(len(dataset[0]))+"\n"
