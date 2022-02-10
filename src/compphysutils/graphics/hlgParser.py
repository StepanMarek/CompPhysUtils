import re
import argparse

convDict = {
    "eV" :  {
        "eV" : 1,
        "H" : 3.6749322175655e-2
    },
    "H" : {
        "eV" : 27.211386245988,
        "H" : 1
    }
}

def hlgLine(textline, energyValMatcher, energyUnitMatcher, occupationMatcher, outputUnit="ev"):
    splitLine = textline.split(",")
    spin = splitLine[2].split(":")[1].strip()
    energy = float(energyValMatcher.search(splitLine[3]).group(0))
    occupation = 0
    if occupationMatcher.search(splitLine[3]):
        if spin == "mos":
            occupation = 2
        else:
            occupation = 1
    fileUnit = energyUnitMatcher.search(splitLine[3]).group(0).strip()
    convFactor = convDict[fileUnit][outputUnit]
    return [energy*convFactor, occupation]

def initParserObjects(parserArgs):
    energyValMatcher = re.compile("[-]?[0-9]*\.[0-9]*e?[\+\-0-9]*")
    energyUnitMatcher = re.compile(" H|(eV)")
    occupationMatcher = re.compile("Occupied")
    ap = argparse.ArgumentParser()
    ap.add_argument("--unit", default="eV", help="Unit for the output")
    outputUnit = ap.parse_args(parserArgs.split()).unit
    return energyValMatcher, energyUnitMatcher, occupationMatcher, outputUnit
