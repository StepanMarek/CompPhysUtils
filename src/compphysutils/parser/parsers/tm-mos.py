import re
import argparse

class TMMosReadingState:
    # Object that ensures that only the converged eigenvalues are read
    # TODO : Read format from the header
    def __init__(self, parserArgs=[]):
        self.orbitalCharRe = re.compile("\s*[\d]+\s*[a-z0-9]+\s*eigenvalue=([\-\.\dD\+]+)\s*nsaos=([\d]+)")
        ap = argparse.ArgumentParser()
        ap.add_argument("--unit", help="Default unit to be used.", default="H")
        ap.add_argument("--format", help="FORTRAN/C format of the output floats", default="4d20.14")
        ap.add_argument("--energyColumn", help="Whether to include the orbital energy at zeroth column, default false", action="store_true")
        self.args = ap.parse_args(parserArgs)
        self.energyUnit = self.args.unit
        self.format = self.args.format
        self.entriesRemaining = 0
        formatSplitOne = self.format.split("d")
        formatSplitTwo = formatSplitOne[1].split(".")
        self.maxNumsPerLine = int(formatSplitOne[0])
        self.charsPerNum = int(formatSplitTwo[0])

    def convertNumber(self, numberString):
        # change D to e
        newString = numberString.replace("D", "e")
        # convert - to -0
        if newString[0] == "-":
            newString = "-0" + newString[1:]
        # convert to float
        # TODO - is this sufficient precision?
        return float(newString)

    def addOrbital(self, nsaos, energy=0):
        # Renew the storage
        self.orbitalEntries = []
        # Set size tracking
        self.entriesRemaining = nsaos
        # If required, output energy
        if self.args.energyColumn:
            self.orbitalEntries.append(energy)

    def addNumEntry(self, numEntry):
        # Append to storage
        self.orbitalEntries.append(numEntry)
        # Decrease tracking
        self.entriesRemaining -= 1
        # Check error
        if self.entriesRemaining < 0:
            raise IndexError("During reading of mos, more entries than declared nsaos registered - check the mos file.")
        # Check print
        if self.entriesRemaining == 0:
            return True
        # In all other cases return false
        return False

def line(line, readState):
    # Check whether line is comment or not
    if line[0] == "#" or line[0] == "$":
        return False
    # In the main body, print out is skipped until a whole of a single orbital is loaded in Reading state, then the whole orbital is output
    # In order to do that, it is necessary to know the nsaos, which is read from the characterisation of orbitals
    orbCharResults = readState.orbitalCharRe.search(line)
    if orbCharResults:
        orbEnergy = readState.convertNumber(orbCharResults.group(1))
        nsaos = int(orbCharResults.group(2))
        readState.addOrbital(nsaos, energy=orbEnergy)
        # After the setup, continue to another line
        return False
    # Only remaining possibility is a line with numbers
    # Start by getting the number of numbers
    numEntries = len(line) // readState.charsPerNum
    for i in range(numEntries):
        numEntry = readState.convertNumber(line[i*readState.charsPerNum:(i+1)*readState.charsPerNum])
        if readState.addNumEntry(numEntry):
            # Ready to print
            return readState.orbitalEntries

def initParserObjects(parserArgs):
    return [TMMosReadingState(parserArgs)]

argDefaults = ""

class TMMosWritingState:
    # Stores information necessary for writing of mos file

    def initiate(self, dataset):
        # Setup format, gain nsaos, check that energy is present
        if len(dataset) != len(dataset[0])+1:
            raise ValueError("TMMosWritingState : Number of columns - 1 : "+str(len(dataset)-1)+" Number of rows : "+str(len(dataset[0]))+" is inconsistent - is the energy column present?")
        # Consistent, define nsaos
        self.nsaos = len(dataset[0])
        # Only works with c1 symmetry group <- TODO
        self.symmetrySpecies = "a"
        # Assumes standard format
        self.format = "4d20.14"
        self.numberFormatEdited = self.format.split("d")[1].split(".")
        self.numberFormatEdited = self.numberFormatEdited[0] + "." + str(int(self.numberFormatEdited[1])-1)
        self.currentOrbIndex = 0

    def writeNumber(self, number):
        # Start by writing native python output, but due to shifting, decrease the number behind decimal point by one
        pythonOutput = ("{:+"+self.numberFormatEdited+"E}").format(number)
        # This format is different on two fronts
        # - it uses 'E' instead of 'D', which tm uses
        # - it always prepends the sign, while TM uses - and 0
        # Start by shifting the decimal point
        newString = "."+pythonOutput[1]+pythonOutput[3:]
        # Now, need to update the exponent
        newString = newString[0:-3] + "{:+03d}".format(int(newString[-3:])+1)
        # Now, append relevant sign
        if pythonOutput[0] == "-":
            newString = "-" + newString
        else:
            newString = "0" + newString
        # Finally, change 'E' for 'D'
        newString = newString.replace("E", "D")
        return newString

    def writeNextOrbChar(self, datarow):
        # Increment after writing out
        orbEnergy = datarow[0]
        output = ("{:6d}{:>3}      eigenvalue="+self.writeNumber(orbEnergy)+"   nsaos={:d}\n").format(self.currentOrbIndex+1, self.symmetrySpecies, self.nsaos)
        self.currentOrbIndex += 1
        return output

# Writing the mos requires energies
def writeLine(datarow, state):
    output = state.writeNextOrbChar(datarow)
    onRow = 0
    # First entry is energy
    index = 1
    while(index < state.nsaos+1):
        output += state.writeNumber(datarow[index])
        index += 1
        onRow += 1
        if onRow >= int(state.format.split("d")[0]):
            onRow = 0
            if index < state.nsaos+1:
                output += "\n"
    return output

def writeHeaders(dataset, state):
    state.initiate(dataset)
    return "$scfmo   expanded   format("+state.format+")"

def writeFooters(dataset, state):
    return "$end"

def initWriterObjects(parserArgs):
    return [TMMosWritingState()]
