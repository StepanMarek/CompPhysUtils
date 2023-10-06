"""
Uses format as specified by
http://paulbourke.net/dataformats/cube/
Only uses Bohr units as output, as this is supported by VESTA
"""
import argparse

bohrToAngstrom = 0.529177210903
elemDict = {
    "h" : 1,
    "c" : 6,
    "o" : 8,
    "na" : 11,
    "au" : 79
}
elemDictInv = {}
for i in elemDict:
    elemDictInv[elemDict[i]] = i

def initParserObjects(parserArgs):
    return {"linesRead" : 0, "atomNum" : 0}

def line(textline, infoObject):
    currLine = infoObject["linesRead"]
    if currLine < 2:
        # Skip the initial information only lines
        infoObject["linesRead"] += 1
        return False
    fields = textline.split()
    if currLine == 2:
        # Read the number of atoms
        infoObject["atomNum"] = int(fields[0])
        infoObject["linesRead"] += 1
        return False
    if currLine in (3,4,5):
        # Only volumetric data box shape
        infoObject["linesRead"] += 1
        return False
    if currLine < 6 + infoObject["atomNum"]:
        # Here, can finally read atom positions
        datarow = []
        # append positions, in Angström
        for i in range(2,5):
            datarow.append(float(fields[i]) * bohrToAngstrom)
        # append element name
        datarow.append(elemDictInv[fields[0]])
        infoObject["linesRead"] += 1
    return datarow

def initWriterObjects(parserArgs):
    ap = argparse.ArgumentParser()
    ap.add_argument("--floatFormat", default="{:> 20.12E}", help="Float format used. Default : {:> 20.12E}")
    ap.add_argument("--intFormat", default="{:> 6d}", help="Integer format used. Default : {:> 6d}")
    args = ap.parse_args(parserArgs)
    return [args]

def writeLine(datarow, args):
    # Assumes standard format for coord data
    # Assumes uncharged species
    # Assumes input in Angströms TODO : accept other input units
    return (args.intFormat + args.floatFormat*4).format(elemDict[datarow[3].lower()], 0.0, *list(map(lambda x: x/bohrToAngstrom, datarow[0:3])))

def writeHeaders(dataset, args):
    return args.intFormat.format(len(dataset[0]))
