import matplotlib.pyplot as plt
from ..parser.parser import parseDatasetConfig
from ..parser.parser import writeParseFunctions 
from ..parser.parser import writeHeaderFunctions 
from ..parser.parser import writeFooterFunctions 
from ..parser.savepoint import parse as savepointParse 
import configparser
from ..parser.combine import commands
from ..parser.combine import runGroupData
from .fitter import plotFit 
from .transformer import transforms
from .decorator import decorations
import importlib
import os

# Search for default plot types
roots = []
modFilenames = []
root, _, filenames = next(os.walk(os.path.dirname(__file__)+"/plot_types"))
roots.append(root)
modFilenames.append(filenames)
# Search for custom plot types
if os.path.isdir(os.path.expanduser("~/.config/compphysutils/plot_types")):
    root, _, filenames = next(os.walk(os.path.expanduser("~/.config/compphysutils/plot_types")))
    roots.append(root)
    modFilenames.append(filenames)
# Import all plot types
plotTypes = {}
for i in range(len(roots)):
    for filename in modFilenames[i]:
        plotTypeName = filename.split(".")[0]
        if plotTypeName[0:2] == "__":
            # Skip __init__.py and similar commands
            continue
        spec = importlib.util.spec_from_file_location("compphysutils.graphics.plot_types."+plotTypeName, roots[i]+"/"+filename)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        plotTypes[plotTypeName] = mod.plot

class ColorIterator:
    def __init__(self, singleCycle="b"):
        self.singleCycle = singleCycle.split()
        self.currentIndex = 0
        self.cycleLen = len(self.singleCycle)

    def __iter__(self):
        return self

    def __next__(self):
        returnVal = self.singleCycle[self.currentIndex % self.cycleLen]
        self.currentIndex += 1
        return returnVal

class LinestyleIterator:
    def __init__(self, singleCycle="solid"):
        self.singleCycle = singleCycle.split()
        self.currentIndex = 0
        self.cycleLen = len(self.singleCycle)

    def __iter__(self):
        return self

    def __next__(self):
        returnVal = self.singleCycle[self.currentIndex % self.cycleLen]
        self.currentIndex += 1
        return returnVal

def plot(datasets, plotType="line", axes=False, **plotOptions):
    if not axes:
        axes = plt.gca()
    if plotType in plotTypes:
        plotTypes[plotType](datasets, axes, **plotOptions)
    else:
        # Defaults to scatter
        plotTypes["scatter"](datasets, axes, **plotOptions)
    axes.set_xlabel(plotOptions["xlabel"])
    axes.set_ylabel(plotOptions["ylabel"])
    if plotOptions["xlim"]:
        axes.set_xlim(*plotOptions["xlim"])
    if plotOptions["ylim"]:
        axes.set_ylim(*plotOptions["ylim"])
    # Insert tick labels
    if plotOptions["xticks"]:
        axes.set_xticks(plotOptions["xticks"][0], labels=plotOptions["xticks"][1])
    if plotOptions["yticks"]:
        axes.set_yticks(plotOptions["yticks"][0], labels=plotOptions["yticks"][1])
    return axes

def fromConfig(configFileName, axes=False, datasets={}):
    axesGiven = False
    if axes:
        axesGiven = True
    cfg = configparser.ConfigParser()
    cfg.read(configFileName)
    datasets.update(runGroupData(cfg, datasets, configFileName))
    # Now, run any transform commands
    if "transform" in cfg["plot"]:
        transformCommands = cfg["plot"].get("transform").split("\n")
        for commandLine in transformCommands:
            commandSplitLine = commandLine.split()
            commandName = commandSplitLine[0]
            datasets = transforms[commandName](datasets, commandSplitLine[1:])
    if "savepoint" in cfg["plot"]:
        savepointParse(cfg["plot"].get("savepoint"), "transform", datasets, writeParseFunctions, writeHeaderFunctions, writeFooterFunctions, "data_transform.out")
    # Now, datasets are complete, and we can read the plot group
    # Also include options that are set directly via type - should be reserved for options that are not usable for many plot types
    graphTypeSplit = cfg["plot"].get("type", "scatter").split()
    graphType = graphTypeSplit[0]
    colCoords = cfg.get("plot", "cols").split("\n")
    for i in range(len(colCoords)):
        colCoords[i] = colCoords[i].split()
    chosenDatasets = []
    for i in range(len(colCoords)):
        chosenDatasets.append([])
        for j in range(0,len(colCoords[i]),2):
            chosenDatasets[i].append(datasets[colCoords[i][j]][int(colCoords[i][j+1])])
    plotOptions = {}
    plotOptions["plotArgString"] = graphTypeSplit[1:]
    plotOptions["legend"] = cfg["plot"].getboolean("legend", True)
    plotOptions["legend-pos"] = cfg["plot"].get("legend-pos", "best")
    plotOptions["legend-cols"] = int(cfg["plot"].get("legend-cols", 1))
    if "xlim" in cfg["plot"]:
        plotOptions["xlim"] = list(map(float, cfg["plot"].get("xlim").split()))
    else:
        plotOptions["xlim"] = False
    if "ylim" in cfg["plot"]:
        plotOptions["ylim"] = list(map(float, cfg["plot"].get("ylim").split()))
    else:
        plotOptions["ylim"] = False
    if "font" in cfg["plot"]:
        plt.rcParams["font.family"] = cfg["plot"].get("font", "sans")
    if "font-size" in cfg["plot"]:
        plt.rcParams["font.size"] = int(cfg["plot"].get("font-size", 12))
    if "mathfont" in cfg["plot"]:
        plt.rcParams["mathtext.fontset"] = cfg["plot"].get("mathfont", "cm")
    plotOptions["colorCycle"] = cfg["plot"].get("colorCycle", "b")
    plotOptions["colorCycle"] = ColorIterator(plotOptions["colorCycle"])
    plotOptions["linestyleCycle"] = cfg["plot"].get("linestyleCycle", "solid")
    plotOptions["linestyleCycle"] = LinestyleIterator(plotOptions["linestyleCycle"])
    plotOptions["xlabel"] = cfg["plot"].get("xlabel", None)
    plotOptions["ylabel"] = cfg["plot"].get("ylabel", None)
    plotOptions["figfile"] = cfg["plot"].get("figfile", False)
    # Dataset labels
    plotOptions["datasetLabels"] = cfg["plot"].get("labels", False)
    if plotOptions["datasetLabels"]:
        plotOptions["datasetLabels"] = plotOptions["datasetLabels"].split("\n")
        if len(plotOptions["datasetLabels"]) < len(colCoords):
            toAdd = len(colCoords) - len(plotOptions["datasetLabels"])
            for i in range(toAdd):
                plotOptions["datasetLabels"].append(None)
    # Arguments supplied are the dataset name, convert it to a dataset that is then plotted
    for ticksName in ["xticks", "yticks"]:
        plotOptions[ticksName] = cfg["plot"].get(ticksName, False)
        if plotOptions[ticksName]:
            plotOptions[ticksName] = datasets[plotOptions[ticksName]]
    axes = plot(chosenDatasets, graphType, axes=axes, **plotOptions)
    # If fit is present, handle it
    fitIndex = 0
    if cfg["plot"].get("fit", False):
        fitLabels = cfg["plot"].get("fit-labels", False)
        numFits = len(cfg["plot"].get("fit").split("\n"))
        if not fitLabels:
            fitLabels = [False] * numFits
        else:
            fitLabels = fitLabels.split("\n")
        if len(fitLabels) < numFits:
            fitLabels += [False] * (numFits - len(fitLabels))
        prevFitParams = []
        fitColorIterator = ColorIterator(cfg["plot"].get("fit-colorCycle", "tab:blue tab:orange tab:green tab:cyan"))
        for allFitArgs in cfg["plot"].get("fit").split("\n"):
            fitArgs = allFitArgs.split()
            # TODO : Fit args?
            prevFitParams += list(plotFit(
                chosenDatasets[int(fitArgs[1])],
                fitArgs[0],
                axes,
                fitPoints=int(cfg["plot"].get("fit-points", 100)),
                fitLabel=fitLabels[fitIndex],
                showParams=cfg["plot"].getboolean("fit-show-params", True),
                fitColorCycle=fitColorIterator,
                paramsPlacement=cfg["plot"].get("params-placement", False),
                paramsOffset=len(prevFitParams),
                xMin=float(cfg["plot"].get("fit-xmin", False)),
                xMax=float(cfg["plot"].get("fit-xmax", False)),
                dirtyRun=cfg["plot"].getboolean("fit-dirty-run", False)
                ))
            fitIndex += 1
    # Handle decorations for main axes
    if cfg["plot"].get("decorate", False):
        decorationCommands = cfg["plot"].get("decorate").split("\n")
        for decorationArgs in decorationCommands:
            decorationSplit = decorationArgs.split()
            axes, datasets = decorations[decorationSplit[0]](axes, datasets, decorationSplit[1:])
    # Move the legend render here, even after decorations (which can also be annotated)
    if plotOptions["legend"]:
        axes.legend(loc=plotOptions["legend-pos"], ncol=plotOptions["legend-cols"])
    # If an inset directive is present, add an inset to the current axes
    if cfg["plot"].get("inset", False):
        insetArgs = cfg["plot"].get("inset").split()
        # Arguments are xpos, ypos, xwidth, ywidth
        insetAxes = axes.inset_axes(list(map(float, insetArgs[1:])))
        fromConfig(insetArgs[0], axes=insetAxes, datasets=datasets)
    # If axes are provided, assume figure is printed somewhere else
    # TODO : Is this a reasonable assumption?
    if axesGiven:
        return True
    if plotOptions["figfile"]:
        plt.savefig(plotOptions["figfile"], bbox_inches="tight")
    else:
        plt.show()
