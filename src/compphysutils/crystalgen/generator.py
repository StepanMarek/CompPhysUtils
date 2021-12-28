from .readCrystalChar import readCrystalChar
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

def generateCrystal(crystalCharFilename, layers=1):
    basisReal, basisRep, unitLength, elemName = readCrystalChar(crystalCharFilename)
    unitBasis = getUnitBasis(len(basisRep))
    crystalRep = generateNLevels(layers, unitBasis, basisRep)
    crystal = getRealStructure(crystalRep, basisReal)
    # Finally, convert to standard format - atomic data format and multiply by unitLength
    data = []
    for pos in crystal:
        data.append(list((unitLength * pos).components) + [elemName])
    return data
