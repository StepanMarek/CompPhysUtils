from scipy.optimize import curve_fit
from .. import __user_conf_dir
import math
import importlib
import os

roots = []
modFilenames = []
root, _, filenames = next(os.walk(os.path.dirname(__file__)+"/fit_types"))
roots.append(root)
modFilenames.append(filenames)
## Search for custom post_process commands
if os.path.isdir(os.path.expanduser(__user_conf_dir+"/fit_types")):
    root, _, filenames = next(os.walk(os.path.expanduser(__user_conf_dir+"/fit_types")))
    roots.append(root)
    modFilenames.append(filenames)
## Import all commands
fitFunctions = {}
guessFunctions = {}
paramNames = {}
fitModules = {}
for i in range(len(roots)):
    for filename in modFilenames[i]:
        fitFuncName = filename.split(".")[0]
        if fitFuncName[0:2] == "__":
            # Skip __init__.py and similar commands
            continue
        spec = importlib.util.spec_from_file_location("compphysutils.graphics.fit_types."+fitFuncName, roots[i]+"/"+filename)
        mod = importlib.util.module_from_spec(spec)
        fitModules[fitFuncName] = {"spec" : spec, "module" : mod, "loaded" : False}

def loadFitType(fitFuncName):
    if not fitFuncName in fitModules:
        raise ModuleNotFoundError("Fit module "+fitFuncName+" was not found in the search tree!")
    fitModules[fitFuncName]["spec"].loader.exec_module(fitModules[fitFuncName]["module"])
    targetModule = fitModules[fitFuncName]["module"]
    fitFunctions[fitFuncName] = targetModule.fit
    paramNames[fitFuncName] = targetModule.paramNames
    if hasattr(targetModule, "guess"):
        guessFunctions[fitFuncName] = targetModule.guess
    else:
        guessFunctions[fitFuncName] = False
    fitModules[fitFuncName]["loaded"] = True

def roundSignificantFigures(number, sigFigs, matchOrder=False):
    if not matchOrder:
        # Default behaviour - match to given number of significant figures
        try:
            result = round(number, sigFigs - 1 - math.floor(math.log10(abs(number))))
        except OverflowError:
            # Number is infinity, just output infinity
            result = "Infinity"
    else:
        # Match to the order of the sigFigs argument
        # Problem is that the variance may be very high
        try:
            result = round(number, -math.floor(math.log10(abs(sigFigs))))
        except OverflowError:
            # Infinity - return number rounded to one significant figure
            try:
                result = round(number, -math.floor(math.log10(abs(number))))
            except OverflowError:
                # If even this overflows, number is infinity, can just output infinity
                result = "Infinity"
    return result

def plotFit(dataset, fitFunctionName, axisObj, **fitParams):
    # Behaviour changes depending on the number of columns
    # TODO : Do other possibilities (i.e. xerr and yerr and no error)
    # Find the indices for the required coordinates
    if not fitModules[fitFunctionName]["loaded"]:
        loadFitType(fitFunctionName)
    ixMin = 0
    if fitParams["xMin"]:
        while fitParams["xMin"] > dataset[0][ixMin]:
            ixMin += 1
    ixMax = len(dataset[0])-1
    if fitParams["xMax"]:
        while fitParams["xMax"] < dataset[0][ixMax]:
            ixMax -= 1
    # Guess the initial params for faster fitting (or succesfull fitting at all)
    guesses = None
    if guessFunctions[fitFunctionName]:
        guesses = guessFunctions[fitFunctionName](dataset[0][ixMin:ixMax+1], dataset[1][ixMin:ixMax+1])
    if fitParams["dirtyRun"]:
        popt = guesses
        perr = guesses
    else:
        try:
            if len(dataset) == 3:
                popt, pcov = curve_fit(fitFunctions[fitFunctionName], dataset[0][ixMin:ixMax+1], dataset[1][ixMin:ixMax+1], sigma=dataset[2][ixMin:ixMax+1], p0=guesses)
            else:
                popt, pcov = curve_fit(fitFunctions[fitFunctionName], dataset[0][ixMin:ixMax+1], dataset[1][ixMin:ixMax+1], p0=guesses)
        except RuntimeError:
            raise RuntimeError(f'Did not manage to find params for fit {fitParams["fitIndex"]}')
        perr = []
        for i in range(len(pcov)):
            perr.append(pcov[i][i] ** 0.5)
    xMin = dataset[0][ixMin]
    xMax = dataset[0][ixMax]
    dx = (xMax - xMin) / (fitParams["fitPoints"] - 1)
    xs = []
    ys = []
    for i in range(fitParams["fitPoints"]):
        xs.append(xMin + dx*i)
        ys.append(fitFunctions[fitFunctionName](xMin + dx*i, *popt))
    if fitParams["fitLabel"]:
        axisObj.plot(xs,ys,label=fitParams["fitLabel"],color=next(fitParams["fitColorCycle"]),ls=next(fitParams["fitLinestyleCycle"]))
    else:
        axisObj.plot(xs,ys,color=next(fitParams["fitColorCycle"]),ls=next(fitParams["fitLinestyleCycle"]))
    # Construct the param string
    if fitParams["showParams"]:
        pstring = ""
        for i in range(len(popt)):
            result = roundSignificantFigures(popt[i], perr[i], matchOrder=True)
            error = roundSignificantFigures(perr[i], 1)
            if fitParams["showError"]:
                pstring += paramNames[fitFunctionName][i]+" : "+str(result)+r"$\pm$"+str(error)+"\n"
            else:
                pstring += paramNames[fitFunctionName][i]+" : "+str(result)+"\n"
        if fitParams["paramsPlacement"]:
            # Text anchor is the bottom left corner by default
            if fitParams["paramsPlacement"] == "tl":
                axisObj.text(0.1, 0.9-0.07*(len(popt)-1)-0.07*(fitParams["paramsOffset"]), pstring, transform=axisObj.transAxes)
        else:
            # Default to top left
            axisObj.text(1.1, 0.9-0.07*(len(popt)-1)-0.07*(fitParams["paramsOffset"]), pstring, transform=axisObj.transAxes)
    return popt, perr
