import re

class EigerReference:
    # Object that ensures that only the converged eigenvalues are read
    def __init__(self, energyUnit="eV"):
        self.reading = False
        self.readingLineRe = re.compile("\s*Nr\.\s*Orbital\s*Occupation\s*Energy")
        self.dataRe = re.compile("(\d+\.\d+)?\s*([\-\+]+\d+\.\d+)[H\s=]*([\-\+]+\d+\.\d+)")
        self.energyUnit = energyUnit

    def testLineReading(self, line):
        resultObj = self.readingLineRe.match(line)
        if resultObj:
            self.reading = True

    def continueReading(self, line):
        resultObj = self.dataRe.search(line)
        if not resultObj:
            self.reading = False
            return False
        energyEv = resultObj.group(3)
        energyH = resultObj.group(2)
        occupation = resultObj.group(1)
        if occupation == None:
            occupation = "0.0"
        if self.energyUnit == "eV":
            return [float(energyEv), float(occupation)]
        else:
            return [float(energyH), float(occupation)]

def eigerLine(line, ER, outputUnit="eV"):
    ER.energyUnit = outputUnit
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

def initParserObjects():
    return [EigerReference()]
