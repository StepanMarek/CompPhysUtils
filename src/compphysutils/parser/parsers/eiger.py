import re
import argparse

class EigerReference:
    # Object that ensures that only the converged eigenvalues are read
    # https://physics.nist.gov/cgi-bin/cuu/Value?hrev
    HtoEv = 27.211386245988

    def __init__(self, parserArgs="--unit eV"):
        self.reading = False
        self.readingLineRe = re.compile("\s*Nr\.\s*Orbital\s*Occupation\s*Energy")
        self.dataRe = re.compile("(\d+\.\d+)?\s*([\-\+]+\d+\.\d+)[H\s=]*([\-\+]+\d+\.\d+)")
        ap = argparse.ArgumentParser()
        ap.add_argument("--unit", help="Unit to be outputed", default="eV")
        self.args = ap.parse_args(parserArgs.split())
        self.energyUnit = self.args.unit

    def testLineReading(self, line):
        resultObj = self.readingLineRe.match(line)
        if resultObj:
            self.reading = True

    def continueReading(self, line):
        resultObj = self.dataRe.search(line)
        if not resultObj:
            self.reading = False
            return False
        energyH = resultObj.group(2)
        occupation = resultObj.group(1)
        if occupation == None:
            occupation = "0.0"
        if self.energyUnit == "eV":
            return [float(energyH)*self.HtoEv, float(occupation)]
        else:
            return [float(energyH), float(occupation)]

def line(line, ER):
    if not ER.reading:
        ER.testLineReading(line)
        return False
    # Reading
    result = ER.continueReading(line)
    if not result:
        # Stop reading
        return False
    # Real result present, convert to floats and return
    return result

def initParserObjects(parserArgs):
    return [EigerReference(parserArgs)]

argDefaults = "--unit eV"
