import importlib
import os

def dynmod(roots, exts):
    mods = {}
    for root in roots:
        _, _, filenames = next(os.walk(os.path.expanduser(root)))
        for filename in filenames:
            filebase, ext = os.path.splitext(filename)
            if ext not in exts or filebase[0:2] == "__":
                continue
            # Setup the import
            modname = os.path.basename(filebase)
            spec = importlib.util.spec_from_file_location(modname, os.path.join(root, filename))
            mod = importlib.util.module_from_spec(spec)
            mods[modname] = {"spec" : spec, "module" : mod, "loaded" : False}
    return mods
