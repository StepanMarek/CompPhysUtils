import random
import configparser
from .readCrystalChar import readCrystalChar, parseCharConfig
from .VectorRepresentation import VectorRepresentation
from .VectorReal import VectorReal

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
        while checkPositionPresent(crystalRep, newVec, basisRep):
            basisIndex = random.randint(0, len(planarBasis)-1)
            newVec = newVec + planarBasis[basisIndex]
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

def generateCrystalRepresentation(basisRep, planarBasis, layers=1, addatoms=0, seed=False):
    unitBasis = getUnitBasis(len(basisRep))
    crystalRep = generateNLevels(layers, unitBasis, basisRep)
    # add-atoms
    crystalRep = addAtoms(crystalRep, basisRep, planarBasis, addatoms, seed=seed)
    return crystalRep

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
    return vectorSum

def createClusterFromConfig(configFilename):
    cfg = configparser.ConfigParser()
    cfg["DEFAULT"] = {"indexdump" : False}
    cfg.read(configFilename)
    if not (("lattice" in cfg["cluster"]) or (("base" in cfg.sections()) and ("vectors" in cfg.sections()))):
        raise ValueError("Missing configuration - need a lattice configuration file [cluster]->lattice or [base] and [vectors] sections in the config file.")
    else:
        if "lattice" in cfg["cluster"]:
            basisReal, basisRep, unitLength, elemName, planarBasis = readCrystalChar(cfg["cluster"]["lattice"])
        else:
            basisReal, basisRep, unitLength, elemName, planarBasis = parseCharConfig(cfg) 
        crystalRep = generateCrystalRepresentation(basisRep, planarBasis, layers=int(cfg["cluster"]["layers"]), addatoms=int(cfg["cluster"]["addatoms"]), seed=cfg["cluster"]["seed"])
        # Start the post-processing
        if "post-processing" in cfg.sections():
            unitBasis = getUnitBasis(len(crystalRep[0].components))
            if "move" in cfg["post-processing"]:
                for movementLine in cfg["post-processing"]["move"].split("\n"):
                    movementInstructions = movementLine.split()
                    vectorSum = postProcessVectorSum(unitBasis, planarBasis, movementInstructions[1:])
                    # Final displacement vector complete - displace the atom
                    crystalRep = moveAtom(crystalRep, basisRep, int(movementInstructions[0]), vectorSum)
            # Movement instructions finished
            if "add" in cfg["post-processing"]:
                for additionLine in cfg["post-processing"]["add"].split("\n"):
                    additionInstructions = additionLine.split()
                    vectorSum = postProcessVectorSum(unitBasis, planarBasis, additionInstructions)
                    crystalRep = addAtomAtPosition(crystalRep, basisRep, vectorSum)
            if "delete" in cfg["post-processing"]:
                for deletionLine in cfg["post-processing"]["delete"].split("\n"):
                    deletionInstructions = deletionLine.split()
                    if deletionInstructions[0] == "index":
                        crystalRep = delAtomAtIndex(crystalRep, int(deletionInstructions[1]))
                    else:
                        vectorSum = postProcessVectorSum(unitBasis, planarBasis, deletionInstructions)
                        crystalRep = delAtomAtPosition(crystalRep, basisRep, vectorSum)
        # Post-processing finished
        structure = getRealStructure(crystalRep, basisReal)
        data = getAtomData(structure, unitLength, elemName)
        # If IndexDump is required, output atom data
        if cfg["post-processing"]["indexdump"]:
            for i in range(len(crystalRep)):
                print(i, crystalRep[i], data[i])
            print("Planar basis")
            for i in range(len(planarBasis)):
                print(i, planarBasis[i])
        saveData(data, cfg["cluster"]["name"])
