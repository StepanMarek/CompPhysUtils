from scipy.optimize import curve_fit
from .. import __user_conf_dir
import math
import importlib
import os
import configparser
from ..util import ColorIterator

from ..util import dynmod

roots = [os.path.dirname(__file__)+"/fit_types", __user_conf_dir+"/fit_types"]

fit_modules = dynmod(roots, [".py"])

fit_functions = {}
param_names = {}
guess_functions = {}

def load_fit_type(fit_type):
    if not fit_type in fit_modules:
        raise ModuleNotFoundError("Fit module "+fit_type+" was not found in the search tree!")
    fit_modules[fit_type]["spec"].loader.exec_module(fit_modules[fit_type]["module"])
    target_module = fit_modules[fit_type]["module"]
    fit_functions[fit_type] = target_module.fit
    param_names[fit_type] = target_module.paramNames
    if hasattr(target_module, "guess"):
        guess_functions[fit_type] = target_module.guess
    else:
        guess_functions[fit_type] = False
    fit_modules[fit_type]["loaded"] = True

def round_significant_figures(number, sig_figs, match_order=False):
    if not match_order:
        # Default behaviour - match to given number of significant figures
        try:
            result = round(number, sig_figs - 1 - math.floor(math.log10(abs(number))))
        except OverflowError:
            # Number is infinity, just output infinity
            result = "Infinity"
    else:
        # Match to the order of the sig_figs argument
        # Problem is that the variance may be very high
        try:
            result = round(number, -math.floor(math.log10(abs(sig_figs))))
        except OverflowError:
            # Infinity - return number rounded to one significant figure
            try:
                result = round(number, -math.floor(math.log10(abs(number))))
            except OverflowError:
                # If even this overflows, number is infinity, can just output infinity
                result = "Infinity"
    return result

def fit_dataset(dataset, fit_type, **fit_params):
    if not fit_modules[fit_type]["loaded"]:
        load_fit_type(fit_type)
    i_xmin = 0
    if fit_params["xmin"]:
        while fit_params["xmin"] > dataset[0][i_xmin] and i_xmin < len(dataset[0]):
            i_xmin += 1
    i_xmax = len(dataset[0])-1
    if fit_params["xmax"]:
        while fit_params["xmax"] < dataset[0][i_xmax] and i_xmax > 0:
            i_xmax -= 1
    guesses = None
    if guess_functions[fit_type]:
        guesses = guess_functions[fit_type](dataset[0][i_xmin:i_xmax+1], dataset[1][i_xmin:i_xmax+1])
    if fit_params["dirty_run"]:
        popt = guesses
        perr = [math.inf]*len(guesses)
        return popt, perr, dataset[0][i_xmin], dataset[0][i_xmax]
    # Continue with standard fitting otherwise
    try:
        if len(dataset) == 3:
            # Including error bars on y
            popt, pcov = curve_fit(fit_functions[fit_type],
                                   dataset[0][i_xmin:i_xmax+1],
                                   dataset[1][i_xmin:i_xmax+1],
                                   sigma=dataset[2][i_xmin:i_xmax+1],
                                   p0=guesses)
        else:
            popt, pcov = curve_fit(fit_functions[fit_type],
                                   dataset[0][i_xmin:i_xmax+1],
                                   dataset[1][i_xmin:i_xmax+1],
                                   p0=guesses)
    except RuntimeError:
        raise RuntimeError(f"Did not manage to find parameters for fit {fit_params['fit_index']}")
    perr = []
    for i in range(len(pcov)):
        perr.append(pcov[i][i] ** 0.5)
    return popt, perr, dataset[0][i_xmin], dataset[0][i_xmax]

def interpolate_fit(fit_type, popt, xmin, xmax, npoints=100):
    dx = (xmax - xmin)/(npoints - 1)
    y = [fit_functions[fit_type](xmin, *popt)]
    x = [xmin]
    for i in range(1,npoints):
        x.append(xmin + i*dx)
        y.append(fit_functions[fit_type](x[-1], *popt))
    return x, y

def from_config(configname, datasets):
    # Returns array of objects, which contain fitted parametrs, their names, and fit labels, i.e. ready for saving/plotting
    cfg = configparser.ConfigParser()
    cfg.read(configname)
    fit_results = []
    if "fit" in cfg:
        # Determine the fit datasets
        fit_dataset_cols = cfg["fit"].get("cols", False)
        if type(fit_dataset_cols) != bool:
            # Some datasets
            fit_dataset_cols = fit_dataset_cols.split("\n")
            for i in range(len(fit_dataset_cols)):
                fit_dataset_cols[i] = fit_dataset_cols[i].split()
            fit_datasets = []
            for i in range(len(fit_dataset_cols)):
                if len(fit_dataset_cols[i]) == 1:
                    # Assumed dataset shape : x,y
                    fit_datasets.append([
                        datasets[fit_dataset_cols[i][0]][0],
                        datasets[fit_dataset_cols[i][0]][1]
                    ])
                elif len(fit_dataset_cols[i]) > 1:
                    # Columns individually specified
                    fit_datasets.append([
                        datasets[fit_dataset_cols[i][0]][int(fit_dataset_cols[i][1])],
                        datasets[fit_dataset_cols[i][2]][int(fit_dataset_cols[i][3])],
                    ])
                else:
                    raise ValueError("Not enough columns provide in fit.")
                if len(fit_dataset_cols[i]) > 4:
                    # Add errors
                    fit_datasets[-1].append(
                        datasets[fit_dataset_cols[i][4]][int(fit_dataset_cols[i][5])]
                    )
            # Fit datasets are ready
            # Fit types are required -- either just one for all datasets or every dataset has specific
            nfits = len(fit_datasets)
            fit_types = cfg["fit"].get("types", "linear").split("\n")
            if len(fit_types) > 1 and len(fit_types) < len(fit_datasets):
                raise ValueError("Did not specify fit type for every fit dataset -- either specify just one for all datasets or assing fit to each dataset.")
            # Retrieve global fit params
            fit_params = {}
            fit_params["dirty_run"] = cfg["fit"].getboolean("dirty_run", False)
            fit_params["show_params"] = cfg["fit"].getboolean("show_params", False)
            # Other fit params are per-fit
            xmins = [None] * nfits
            xmaxs = [None] * nfits
            if cfg["fit"].get("xlims", False):
                xlims = cfg["fit"].get("xlims").split("\n")
                for i in range(len(xlims)):
                    xlim_split = xlims[i].split()
                    xmins[i] = float(xlim_split[0])
                    xmaxs[i] = float(xlim_split[1])
            labels = [None] * nfits
            if cfg["fit"].get("labels", False):
                label_split = cfg["fit"].get("labels").split("\n")
                for i in range(len(label_split)):
                    labels[i] = label_split[i]
            npoints = [100] * nfits
            npoint_strings = cfg["fit"].get("npoints", "100").split("\n")
            for i in range(len(npoint_strings)):
                if i >= len(npoints):
                    raise ValueError(f"Too many npoints provided for {nfits} fits")
                npoints[i] = int(npoint_strings[i])
            # Color will be determined per-fit
            c_iter = ColorIterator(cfg["fit"].get("color_cycle", "red green blue cyan magenta yellow black"))
            # Continue with fit results population
            for i in range(nfits):
                # TODO : Savepoints, both for interpolations and for parameters
                fit_params["xmin"] = xmins[i]
                fit_params["xmax"] = xmaxs[i]
                popt, perr, xmin, xmax = fit_dataset(fit_datasets[i], fit_types[i], **fit_params)
                text = ""
                for j in range(len(popt)):
                    text += param_names[fit_types[i]][j] + " : "
                    text += str(round_significant_figures(popt[j],perr[j],match_order=True))
                    text += " ± " + str(round_significant_figures(perr[j],1)) + "\n"
                fit_results.append({
                    "popt" : popt,
                    "perr" : perr,
                    "label" : labels[i],
                    "color" : next(c_iter),
                    "text" : text,
                    "interpolation" : interpolate_fit(fit_types[i], popt, xmin, xmax, npoints[i])
                })
    return fit_results


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
