import re
import argparse

class AimsReference:
    # Object that ensures that only the converged eigenvalues are read
    def __init__(self, parserArgs="--unit eV"):
        self.converged = False
        self.reading = False
        self.convergedLineRe = re.compile("Begin\s*self\-consistency\s*iteration\s*#\s*(\d+)")
        self.readingLineRe = re.compile("\s*State\s*Occupation\s*Eigenvalue\s*\[Ha\]\s*Eigenvalue\s*\[eV\]")
        self.dataRe = re.compile("([\d\.]+)\s*([\d\.]+)\s*([\-\d\.]+)\s*([\-\d\.]+)")
        ap = argparse.ArgumentParser()
        ap.add_argument("--unit", help="Default unit to be used.", default="eV")
        self.args = ap.parse_args(parserArgs.split())
        self.energyUnit = self.args.unit

    def testLineConverged(self, line):
        result = self.convergedLineRe.search(line)
        if result and int(result.group(1)) > 1:
            self.converged = True
            return True
        return False

    def testLineReading(self, line):
        resultObj = self.readingLineRe.match(line)
        if resultObj:
            self.reading = True

    def continueReading(self, line):
        resultObj = self.dataRe.search(line)
        if not resultObj:
            self.reading = False
            return False
        energyEv = resultObj.group(4)
        energyH = resultObj.group(3)
        occupation = resultObj.group(2)
        stateIndex = resultObj.group(1)
        if self.energyUnit == "eV":
            return [float(energyEv), float(occupation)]
        else:
            return [float(energyH), float(occupation)]

def line(line, AR):
    if not AR.converged:
        AR.testLineConverged(line)
        return False
    # Converged, or at least candidate converged
    if not AR.reading:
        AR.testLineReading(line)
        return False
    # Reading
    result = AR.continueReading(line)
    if not result:
        # Stop reading
        return False
    # Real result present, convert to floats and return
    return result

def initParserObjects(parserArgs):
    return [AimsReference(parserArgs)]

argDefaults = "--unit eV"
