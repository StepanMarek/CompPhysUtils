import matplotlib.pyplot as plt
from .parser import parseDatasetConfig

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

#TODO : Implement reading of the plotter config file
#def fromConfig(configFileName):
