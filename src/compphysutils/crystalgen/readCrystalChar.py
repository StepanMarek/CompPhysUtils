import configparser
from .VectorReal import VectorReal
from .VectorRepresentation import VectorRepresentation

# TODO : Need to decide about the location of default files containing possible configs and about dir scanning
def parseVectors(vectorsString, representation=False):
    """
    Returns the real/representation vectors based on the files given in the string
    """
    # If the strings are not present, return false
    if not vectorsString:
        return False
    vecs = []
    vecStrings = vectorsString.split()
    if not representation:
        for i in range(len(vecStrings)):
            vecs.append(VectorReal(*map(float, vecStrings[i].split(","))))
    else:
        for i in range(len(vecStrings)):
            vecs.append(VectorRepresentation(*map(int, vecStrings[i].split(","))))
    return vecs

def parseCharConfig(cfg):
    realBasis = parseVectors(cfg["vectors"]["real"])
    reprBasis = parseVectors(cfg["vectors"]["representation"], representation=True)
    planarBasis = parseVectors(cfg["vectors"].get("planar", False), representation=True)
    unitCellLength = float(cfg["base"]["unit"])
    elemName = cfg["base"]["atom"]
    return realBasis, reprBasis, unitCellLength, elemName, planarBasis

def readCrystalChar(filename):
    """
    Returns the representation and real basis of the crystal
    Real basis is still in units of unit cell length
    """
    cfg = configparser.ConfigParser()
    cfg.read(filename)
    return parseCharConfig(cfg)
