import re
import argparse

class ColsReference:
    # Object that ensures that only the converged eigenvalues are read
    def __init__(self, parserArgs=["0"]):
        self.argsReader = argparse.ArgumentParser(description="Parses the arguments for the parser itself.")
        self.argsReader.add_argument("--comment", help="Character to be used as indicator of comment. [default : #]", default="#")
        self.argsReader.add_argument("--skip", type=int, default=0, help="Skip a given number of lines before starting the read.")
        self.argsReader.add_argument("cols", nargs="+", type=int, help="Indices of columns to read.")
        self.args = self.argsReader.parse_args(parserArgs)
        self.skips_remaining = self.args.skip

    def continueReading(self, line):
        stripLine = line.strip()
        if self.skips_remaining > 0:
            self.skips_remaining -= 1
            return False
        if len(stripLine) == 0:
            # Do not attempt to read empty lines
            return False
        if stripLine[0] == self.args.comment:
            return False
        # Not commented, read
        # TODO : Different var types
        splitLine = stripLine.split()
        retVal = []
        for i in self.args.cols:
            retVal.append(float(splitLine[i]))
        return retVal

def line(line, CR):
    # Reading
    result = CR.continueReading(line)
    if not result:
        # Stop reading
        return False
    # Real result present, convert to floats and return
    return result

def initParserObjects(parserArgs):
    return [ColsReference(parserArgs)]

argDefaults = "0"

def writeLine(datarow):
    datalist = list(map(str, datarow))
    return " ".join(datalist)
