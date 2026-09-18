import importlib
import os
import inspect

def dynmod(roots, exts):
    """
    Returns the dictionary of all modules for compphysutils from given roots
    which can be dynamically loaded
    """
    mods = {}
    for root in roots:
        exp_root = os.path.expanduser(root)
        if not os.path.isdir(exp_root):
            continue
        _, _, filenames = next(os.walk(exp_root))
        for filename in filenames:
            filebase, ext = os.path.splitext(filename)
            if ext not in exts or filebase[0:2] == "__":
                continue
            # Setup the import
            modname = os.path.basename(filebase)
            spec = importlib.util.spec_from_file_location(modname, os.path.join(exp_root, filename))
            mod = importlib.util.module_from_spec(spec)
            mods[modname] = {"spec" : spec, "module" : mod, "loaded" : False}
    return mods

def modcheck(mod, member):
    """
    Check whether a given member (given by a string) is present in the module
    Returns False if not present, otherwise returns the member
    """
    inspection = inspect.getmembers(mod)
    for name, val in inspection:
        if name == member:
            return val
    # No such member found
    return False

class CyclicIterator:
    def __init__(self, cycle=[]):
        self.singleCycle = cycle
        self.cycleLen = len(cycle)
        self.currentIndex = 0

    def __iter__(self):
        return self

    def __next__(self):
        returnVal = self.singleCycle[self.currentIndex % self.cycleLen]
        self.currentIndex += 1
        return returnVal

class ColorIterator(CyclicIterator):
    def __init__(self, singleCycle="b"):
        # Change the format if necessary
        listOfColors = singleCycle.split()
        for i in range(len(listOfColors)):
            if listOfColors[i].find(",") >= 0:
                listOfColors[i] = tuple(map(float, listOfColors[i].split(",")))
        super().__init__(listOfColors)

class LinestyleIterator(CyclicIterator):
    def __init__(self, singleCycle="-"):
        super().__init__(singleCycle.split())

class MarkerstyleIterator(CyclicIterator):
    def __init__(self, singleCycle="o"):
        super().__init__(singleCycle.split())

