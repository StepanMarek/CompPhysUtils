from scipy.optimize import curve_fit
import math

def linFit(x, a, b):
    return a*x + b

def roundSignificantFigures(number, sigFigs, matchOrder=False):
    if not matchOrder:
        # Default behaviour - match to given number of significant figures
        return round(number, sigFigs - 1 - math.floor(math.log10(abs(number))))
    else:
        # Match to the order of the sigFigs argument
        return round(number, -math.floor(math.log10(abs(sigFigs))))

def plotFit(dataset, fitFunctionName, axisObj, **fitParams):
    # Behaviour changes depending on the number of columns
    # TODO : Do other possibilities (i.e. xerr and yerr and no error)
    if len(dataset) == 3:
        popt, pcov = curve_fit(fitFunctions[fitFunctionName], dataset[0], dataset[1], sigma=dataset[2])
    else:
        popt, pcov = curve_fit(fitFunctions[fitFunctionName], dataset[0], dataset[1])
    perr = []
    for i in range(len(pcov)):
        perr.append(pcov[i][i] ** 0.5)
    x0 = min(dataset[0])
    x1 = max(dataset[0])
    y0 = fitFunctions[fitFunctionName](x0, *popt)
    y1 = fitFunctions[fitFunctionName](x1, *popt)
    if fitParams["fitLabel"]:
        axisObj.plot([x0,x1],[y0,y1],label=fitParams["fitLabel"])
    else:
        axisObj.plot([x0,x1],[y0,y1])
    # Construct the param string
    pstring = ""
    for i in range(len(popt)):
        pstring += paramNames[fitFunctionName][i]+" : "+str(roundSignificantFigures(popt[i], perr[i], matchOrder=True))+r"$\pm$"+str(roundSignificantFigures(perr[i],1))+"\n"
    if fitParams["paramsPlacement"]:
        if fitParams["paramsPlacement"] == "tl":
            axisObj.text(0.1, 0.9-0.1*(len(paramNames[fitFunctionName])-1+fitParams["paramsOffset"]), pstring, transform=axisObj.transAxes)
    else:
        # Default to top left
        axisObj.text(0.1, 0.9-0.1*(len(paramNames[fitFunctionName])-1+fitParams["paramsOffset"]), pstring, transform=axisObj.transAxes)
    return popt

fitFunctions = {
    "lin" : linFit
}
paramNames = {
    "lin" : ["Gradient", "Intercept"]
}
