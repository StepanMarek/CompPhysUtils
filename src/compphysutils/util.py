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
