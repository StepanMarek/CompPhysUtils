import re
import argparse

class ColsReference:
    # Object that ensures that only the converged eigenvalues are read
    def __init__(self, parserArgs="0"):
        self.argsReader = argparse.ArgumentParser(description="Parses the arguments for the parser itself.")
        self.argsReader.add_argument("--comment", help="Character to be used as indicator of comment. [default : #]", default="#")
        self.argsReader.add_argument("cols", nargs="+", type=int, help="Indices of columns to read.")
        self.args = self.argsReader.parse_args(parserArgs.split())

    def continueReading(self, line):
        if line[0] == self.args.comment:
            return False
        # Not commented, read
        # TODO : Different var types
        splitLine = line.split(",")
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
