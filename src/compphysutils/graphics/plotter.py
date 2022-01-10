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
        datasetLabels = [False] * len(datasets)
    for dataIndex in range(len(datasets)):
        axisObj.errorbar(datasets[dataIndex][0], datasets[dataIndex][1], xerr=datasets[dataIndex][2], yerr=datasets[dataIndex][3], label=datasetLabels[dataIndex])
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
    elif plotType = "level":
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
        commandName = commandLine[0]
        datasets = commands[commandName](datasets, commandLine[1:])
    # Now, datasets are complete, and we can read the plot group
    # So far, only 2D graphs
    graphType = cfg.get("plot", "type", "scatter")
    colCoords = cfg.get("plot", "cols").split()
    chosenDatasets = []
    for i in range(0,len(colCoords),2):
        chosenDatasets.append(datasets[colCoords[i]][colCoords[i+1]])
    plotOptions = {}
    plotOptions["legend"] = cfg.getboolean("plot", "legend", True)
    plotOptions["xlim"] = list(map(float, cfg.get("plot", "xlim").split()))
    plotOptions["ylim"] = list(map(float, cfg.get("plot", "ylim").split()))
    plotOptions["xlabel"] = cfg.get("plot", "xlabel", "X")
    plotOptions["ylabel"] = cfg.get("plot", "ylabel", "Y")
    plotOptions["figfile"] = cfg.get("plot", "figfile", False)
    plot(chosenDatasets, graphType, **plotOptions)
