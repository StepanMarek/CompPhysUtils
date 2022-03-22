import random
import configparser
from .readCrystalChar import readCrystalChar, parseCharConfig
from .VectorRepresentation import VectorRepresentation
from .VectorReal import VectorReal
import os

def getUnitBasis(N):
    basis = []
    for i in range(N):
        basis.append(VectorRepresentation(*([0]*N)))
        basis[-1].components[i] = 1
    return basis

def checkPositionPresent(crystalRep, vecRep, basisRep):
    for otherRep in crystalRep:
        if vecRep.translateToBasis(basisRep) == otherRep.translateToBasis(basisRep):
            return True
    return False

def generateNextLevel(crystalRep, unitBasis, basisRep):
    """
    Grows the crystal by one layer.
    """
    # Iterate over positions of all atoms
    newLayer = []
    for vecRep in crystalRep:
        # Try adding each basis vector
        for unitRep in unitBasis:
            newVec = vecRep + unitRep
            if checkPositionPresent(crystalRep, newVec,basisRep) or checkPositionPresent(newLayer, newVec, basisRep):
                # Do not add this vector, skip it
                continue
            # Add the vector to the crystal
            newLayer.append(newVec)
    # The argument is augmented and returned
    return crystalRep + newLayer

def addAtoms(crystalRep, basisRep, planarBasis, addatoms, seed=False):
    if seed:
        random.seed(seed)
    for i in range(addatoms):
        # Choose atom at random
        atomIndex = random.randint(0,len(crystalRep)-1)
        newVec = crystalRep[atomIndex]
        # Create 1/-1 multiplier choices
        basisMultipliers = []
        for j in range(len(planarBasis)):
            basisMultipliers.append(random.choice([1,-1]))
        while checkPositionPresent(crystalRep, newVec, basisRep):
            basisIndex = random.randint(0, len(planarBasis)-1)
            newVec = newVec + (basisMultipliers[basisIndex] * planarBasis[basisIndex])
        crystalRep = crystalRep + [newVec]
    return crystalRep

def generateNLevels(N, unitBasis, basisRep):
    crystalRep = [VectorRepresentation(*([0]*len(unitBasis)))]
    for i in range(N-1):
        crystalRep = generateNextLevel(crystalRep, unitBasis, basisRep)
    return crystalRep

def getRealStructure(crystalRep, basisReal):
    crystal = []
    for vecRep in crystalRep:
        crystal.append(vecRep.translateToBasis(basisReal))
    return crystal

def getAtomData(crystal, unitLength, elemName):
    data = []
    for pos in crystal:
        data.append(list((unitLength * pos).components) + [elemName])
    return data

def generateCrystalRepresentation(basisRep, layers=1):
    unitBasis = getUnitBasis(len(basisRep))
    crystalRep = generateNLevels(layers, unitBasis, basisRep)
    # add-atoms
    #if not planarBasis:
    #    crystalRep = addAtoms(crystalRep, basisRep, unitBasis, addatoms, seed=seed)
    #else:
    #    crystalRep = addAtoms(crystalRep, basisRep, planarBasis, addatoms, seed=seed)
    return crystalRep, unitBasis

def generateCrystal(crystalCharFilename, layers=1, addatoms=0, seed=False):
    basisReal, basisRep, unitLength, elemName, planarBasis = readCrystalChar(crystalCharFilename)
    crystalRep = generateCrystalRepresentation(basisRep, planarBasis, layers=layers, addatoms=addatoms, seed=seed)
    crystal = getRealStructure(crystalRep, basisReal)
    # Finally, convert to standard format - atomic data format and multiply by unitLength
    return getAtomData(crystal, unitLength, elemName)

def moveAtom(crystalRep, basisRep, index, vector):
    newVec = crystalRep[index] + vector
    if checkPositionPresent(crystalRep, newVec, basisRep):
        raise ValueError("Atom would be moved to an already occupied crystal site!")
    else:
        crystalRep[index] = newVec
    return crystalRep

def addAtomAtPosition(crystalRep, basisRep, vector):
    if checkPositionPresent(crystalRep, vector, basisRep):
        raise ValueError("Atom would be added to an already occupied crystal site!")
    else:
        crystalRep.append(vector)
    return crystalRep

def delAtomAtPosition(crystalRep, basisRep, vector):
    # Delete if possible, otherwise just raise warning, not exception
    deleted = False
    for i in range(len(crystalRep)):
        if vector == crystalRep[i]:
            del crystalRep[i]
            deleted = True
            break
    if not deleted:
        print("No atom found at position "+str(vector))
    return crystalRep

def delAtomAtIndex(crystalRep, index):
    del crystalRep[index]
    return crystalRep

def getDataString(atomicData):
    string = str(len(atomicData))+"\n\n"
    for i in range(len(atomicData)):
        string = string + atomicData[i][-1].upper()+" "+" ".join(map(str, atomicData[i][:3])) + "\n"
    return string

def printData(atomicData):
    print(getDataString(atomicData))

def saveData(atomicData, filename):
    file = open(filename, "w")
    file.write(getDataString(atomicData))
    file.close()

def postProcessVectorSum(unitBasis, planarBasis, instructions):
    vectorSum = unitBasis[0].cloneZeros()
    for i in range(0,len(instructions),2):
        if instructions[i] == "planar":
            vectorSum = vectorSum + planarBasis[int(instructions[i+1])]
        elif instructions[i] == "basis":
            vectorSum = vectorSum + unitBasis[int(instructions[i+1])]
        elif instructions[i] == "mbasis":
            vectorSum = vectorSum - unitBasis[int(instructions[i+1])]
        elif instructions[i] == "mplanar":
            vectorSum = vectorSum - planarBasis[int(instructions[i+1])]
    return vectorSum

def createClusterFromConfig(configFilename):
    cfg = configparser.ConfigParser()
    cfg.set("DEFAULT", "indexdump", "False")
    cfg.read(configFilename)
    if not (("lattice" in cfg["cluster"]) or (("base" in cfg.sections()) and ("vectors" in cfg.sections()))):
        raise ValueError("Missing configuration - need a lattice configuration file [cluster]->lattice or [base] and [vectors] sections in the config file.")
    else:
        if "lattice" in cfg["cluster"]:
            # Check whether the lattice exists in cwd or in config directory, cwd takes priority
            if os.path.isfile(cfg["cluster"]["lattice"]):
                basisReal, basisRep, unitLength, elemName, planarBasis = readCrystalChar(cfg["cluster"]["lattice"])
            else:
                # Try config dir
                basisReal, basisRep, unitLength, elemName, planarBasis = readCrystalChar(os.path.expanduser("~/.config/compphysutils/lattices/")+cfg["cluster"]["lattice"])
        else:
            basisReal, basisRep, unitLength, elemName, planarBasis = parseCharConfig(cfg)
        crystalRep, unitBasis = generateCrystalRepresentation(basisRep, layers=int(cfg["cluster"]["layers"]), )
        # Remove the atoms if doing a sphere cut
        if "post-process" in cfg.sections():
            if "sphere-cut" in cfg["post-process"]:
                radius = float(cfg["post-process"].get("sphere-cut", 1.0))
                newCrystalRep = []
                for atom in crystalRep:
                    realPos = atom.translateToBasis(basisReal) * unitLength
                    if abs(realPos) <= radius:
                        newCrystalRep.append(atom)
                crystalRep = newCrystalRep
        # add-atoms
        if not planarBasis:
            crystalRep = addAtoms(crystalRep, basisRep, unitBasis, addatoms=int(cfg["cluster"]["addatoms"]), seed=cfg["cluster"].get("seed", False))
        else:
            crystalRep = addAtoms(crystalRep, basisRep, planarBasis, addatoms=int(cfg["cluster"]["addatoms"]), seed=cfg["cluster"].get("seed", False))
        # Start the post-process
        if "post-process" in cfg.sections():
            unitBasis = getUnitBasis(len(crystalRep[0].components))
            if "move" in cfg["post-process"]:
                for movementLine in cfg["post-process"]["move"].split("\n"):
                    movementInstructions = movementLine.split()
                    vectorSum = postProcessVectorSum(unitBasis, planarBasis, movementInstructions[1:])
                    # Final displacement vector complete - displace the atom
                    crystalRep = moveAtom(crystalRep, basisRep, int(movementInstructions[0]), vectorSum)
            # Movement instructions finished
            if "add" in cfg["post-process"]:
                for additionLine in cfg["post-process"]["add"].split("\n"):
                    additionInstructions = additionLine.split()
                    vectorSum = postProcessVectorSum(unitBasis, planarBasis, additionInstructions)
                    crystalRep = addAtomAtPosition(crystalRep, basisRep, vectorSum)
            if "delete" in cfg["post-process"]:
                for deletionLine in cfg["post-process"]["delete"].split("\n"):
                    deletionInstructions = deletionLine.split()
                    if deletionInstructions[0] == "index":
                        crystalRep = delAtomAtIndex(crystalRep, int(deletionInstructions[1]))
                    else:
                        vectorSum = postProcessVectorSum(unitBasis, planarBasis, deletionInstructions)
                        crystalRep = delAtomAtPosition(crystalRep, basisRep, vectorSum)
        structure = getRealStructure(crystalRep, basisReal)
        data = getAtomData(structure, unitLength, elemName)
        # If IndexDump is required, output atom data
        if "post-process" in cfg.sections():
            dumpIndexInfo = cfg.getboolean("post-process", "indexdump")
            if dumpIndexInfo:
                for i in range(len(crystalRep)):
                    print(i, crystalRep[i], data[i])
                if(planarBasis):
                    print("Planar basis")
                    for i in range(len(planarBasis)):
                        print(i, planarBasis[i])
        if "post-process" in  cfg.sections():
            if "random-noise" in cfg["post-process"]:
                # Generate random Gaussian noise with given amplitude for each atom in the system
                # This is applied at the very end in order to allow manipulation of crystal before
                argSplit = cfg["post-process"].get("random-noise").split()
                radius = float(argSplit[0])
                seed = int(argSplit[1])
                random.seed(seed)
                for i in range(len(data)):
                    for j in range(3):
                        data[i][j] += random.gauss(0,radius)
        saveData(data, cfg["cluster"]["name"])
