import matplotlib.pyplot as plt
from .parser import parseDatasetConfig
import configparser
from .combine import commands


def linePlot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [False] * len(datasets)
    for dataIndex in range(len(datasets)):
        axisObj.plot(datasets[dataIndex][0], datasets[dataIndex][1], label=datasetLabels[dataIndex])
    return axisObj

def scatterPlot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [False] * len(datasets)
    for dataIndex in range(len(datasets)):
        axisObj.scatter(datasets[dataIndex][0], datasets[dataIndex][1], label=datasetLabels[dataIndex])
    return axisObj

def errorPlot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        if len(datasets[dataIndex]) >= 4:
            # If at least four columns provided, plot errors on both axes
            axisObj.errorbar(datasets[dataIndex][0], datasets[dataIndex][2], xerr=datasets[dataIndex][1], yerr=datasets[dataIndex][3], label=datasetLabels[dataIndex])
        else:
            # Otherwise, just plot yerr
            axisObj.errorbar(datasets[dataIndex][0], datasets[dataIndex][1], yerr=datasets[dataIndex][2],label=datasetLabels[dataIndex])
    return axisObj

def levelPlot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [False] * len(datasets)
    for dataIndex in range(len(datasets)):
        axisObj.eventplot(datasets[dataIndex][1], lineoffsets=datasets[dataIndex][0], orientation="vertical", label=datasetLabels[dataIndex])
    return axisObj

def plot(datasets, plotType="line", **plotOptions):
    axis = plt.gca()
    if plotType == "line":
        linePlot(datasets, axis, **plotOptions)
    elif plotType == "errorbar":
        errorPlot(datasets, axis, **plotOptions)
    elif plotType == "level":
        levelPlot(datasets, axis, **plotOptions)
    else:
        # Defaults to scatter
        scatterPlot(datasets, axis, **plotOptions)
    plt.xlabel(plotOptions["xlabel"])
    plt.ylabel(plotOptions["ylabel"])
    if plotOptions["legend"]:
        plt.legend()
    if plotOptions["xlim"]:
        plt.xlim(*plotOptions["xlim"])
    if plotOptions["ylim"]:
        plt.ylim(*plotOptions["ylim"])
    if plotOptions["figfile"]:
        plt.savefig(plotOptions["figfile"], bbox_inches="tight")
    else:
        plt.show()

def fromConfig(configFileName):
    cfg = configparser.ConfigParser()
    cfg.read(configFileName)
    # Read the datasets
    datasets = parseDatasetConfig(cfg.get("data", "datasetfile"))
    # Run any combine commands
    combineCommands = cfg.get("data", "combine").split("\n")
    for commandLine in combineCommands:
        commandSplitLine = commandLine.split()
        commandName = commandSplitLine[0]
        datasets = commands[commandName](datasets, commandSplitLine[1:])
    # Now, datasets are complete, and we can read the plot group
    # So far, only 2D graphs
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
    if "xlim" in cfg["plot"]:
        plotOptions["xlim"] = list(map(float, cfg["plot"].get("xlim").split()))
    else:
        plotOptions["xlim"] = False
    if "ylim" in cfg["plot"]:
        plotOptions["ylim"] = list(map(float, cfg["plot"].get("ylim").split()))
    else:
        plotOptions["ylim"] = False
    plotOptions["xlabel"] = cfg["plot"].get("xlabel", "X")
    plotOptions["ylabel"] = cfg["plot"].get("ylabel", "Y")
    plotOptions["figfile"] = cfg["plot"].get("figfile", False)
    # Dataset labels
    plotOptions["datasetLabels"] = cfg["plot"].get("labels", False)
    if plotOptions["datasetLabels"]:
        plotOptions["datasetLabels"] = plotOptions["datasetLabels"].split("\n")
        if len(plotOptions["datasetLabels"]) < len(colCoords):
            toAdd = len(colCoords) - len(plotOptions["datasetLabels"])
            for i in range(toAdd):
                plotOptions["datasetLabels"].append(None)
    plot(chosenDatasets, graphType, **plotOptions)
