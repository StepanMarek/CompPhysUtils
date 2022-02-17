import matplotlib.pyplot as plt
from ..parser.parser import parseDatasetConfig
import configparser
from ..parser.combine import commands
from .fitter import plotFit 
from .transformer import transforms
from .decorator import decorations

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

def linePlot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        axisObj.plot(datasets[dataIndex][0], datasets[dataIndex][1], label=datasetLabels[dataIndex], color=next(plotOptions["colorCycle"]), linestyle=next(plotOptions["linestyleCycle"]))
    return axisObj

def scatterPlot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        axisObj.scatter(datasets[dataIndex][0], datasets[dataIndex][1], label=datasetLabels[dataIndex])
    return axisObj

def errorPlot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        if len(datasets[dataIndex]) >= 4:
            # If at least four columns provided, plot errors on both axes
            axisObj.errorbar(datasets[dataIndex][0], datasets[dataIndex][2], xerr=datasets[dataIndex][1], yerr=datasets[dataIndex][3], capsize=4, lw=0, elinewidth=2, marker="p", ms=1, label=datasetLabels[dataIndex])
        else:
            # Otherwise, just plot yerr
            axisObj.errorbar(datasets[dataIndex][0], datasets[dataIndex][1], yerr=datasets[dataIndex][2], capsize=4, lw=0, elinewidth=2, marker="p", ms=2, label=datasetLabels[dataIndex])
    return axisObj

def levelPlot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        # For x positions, only takes into account first element
        axisObj.eventplot(datasets[dataIndex][1], lineoffsets=datasets[dataIndex][0][0], orientation="vertical", label=datasetLabels[dataIndex], colors=next(plotOptions["colorCycle"]))
    return axisObj

def plot(datasets, plotType="line", axes=False, **plotOptions):
    if not axes:
        axes = plt.gca()
    if plotType == "line":
        linePlot(datasets, axes, **plotOptions)
    elif plotType == "errorbar":
        errorPlot(datasets, axes, **plotOptions)
    elif plotType == "level":
        levelPlot(datasets, axes, **plotOptions)
    else:
        # Defaults to scatter
        scatterPlot(datasets, axes, **plotOptions)
    axes.set_xlabel(plotOptions["xlabel"])
    axes.set_ylabel(plotOptions["ylabel"])
    if plotOptions["legend"]:
        axes.legend(loc=plotOptions["legend-pos"])
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

def fromConfig(configFileName, axes=False):
    axesGiven = False
    if axes:
        axesGiven = True
    cfg = configparser.ConfigParser()
    cfg.read(configFileName)
    datasets = {}
    # Read the datasets
    if "data" in cfg:
        datasetfiles = cfg["data"].get("datasetfiles", False)
        if datasetfiles:
            for datasetFileName in datasetfiles.split("\n"):
                datasets.update(parseDatasetConfig(datasetFileName))
    # In place defined datasets take priority
    datasets.update(parseDatasetConfig(configFileName))
    # Now, run the combine directive, if present
    if "data" in cfg:
        if "combine" in cfg["data"]:
            combineCommands = cfg.get("data", "combine").split("\n")
            for commandLine in combineCommands:
                commandSplitLine = commandLine.split()
                commandName = commandSplitLine[0]
                datasets = commands[commandName](datasets, commandSplitLine[1:])
    # Now, run any transform commands
    if "transform" in cfg["plot"]:
        transformCommands = cfg["plot"].get("transform").split("\n")
        for commandLine in transformCommands:
            commandSplitLine = commandLine.split()
            commandName = commandSplitLine[0]
            datasets = transforms[commandName](datasets, commandSplitLine[1:])
    # Now, datasets are complete, and we can read the plot group
    graphType = cfg["plot"].get("type", "scatter")
    colCoords = cfg.get("plot", "cols").split("\n")
    for i in range(len(colCoords)):
        colCoords[i] = colCoords[i].split()
    chosenDatasets = []
    for i in range(len(colCoords)):
        chosenDatasets.append([])
        for j in range(0,len(colCoords[i]),2):
            chosenDatasets[i].append(datasets[colCoords[i][j]][int(colCoords[i][j+1])])
    plotOptions = {}
    plotOptions["legend"] = cfg["plot"].getboolean("legend", True)
    plotOptions["legend-pos"] = cfg["plot"].get("legend-pos", "upper right")
    if "xlim" in cfg["plot"]:
        plotOptions["xlim"] = list(map(float, cfg["plot"].get("xlim").split()))
    else:
        plotOptions["xlim"] = False
    if "ylim" in cfg["plot"]:
        plotOptions["ylim"] = list(map(float, cfg["plot"].get("ylim").split()))
    else:
        plotOptions["ylim"] = False
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
    if cfg["plot"].get("fit", False):
        fitArgs = cfg["plot"].get("fit").split()
        # TODO : Fit args?
        plotFit(chosenDatasets[int(fitArgs[1])], fitArgs[0], axes, fitLabel=cfg["plot"].get("fit-label", False), paramsPlacement=cfg["plot"].get("params-placement", False))
    # Handle decorations for main axes
    if cfg["plot"].get("decorate", False):
        decorationCommands = cfg["plot"].get("decorate").split("\n")
        for decorationArgs in decorationCommands:
            decorationSplit = decorationArgs.split()
            axes, datasets = decorations[decorationSplit[0]](axes, datasets, decorationSplit[1:])
    # If an inset directive is present, add an inset to the current axes
    if cfg["plot"].get("inset", False):
        insetArgs = cfg["plot"].get("inset").split()
        # Arguments are xpos, ypos, xwidth, ywidth
        insetAxes = axes.inset_axes(list(map(float, insetArgs[1:])))
        fromConfig(insetArgs[0], axes=insetAxes)
    # If axes are provided, assume figure is printed somewhere else
    # TODO : Is this a reasonable assumption?
    if axesGiven:
        return True
    if plotOptions["figfile"]:
        plt.savefig(plotOptions["figfile"], bbox_inches="tight")
    else:
        plt.show()
