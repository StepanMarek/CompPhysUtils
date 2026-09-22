def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        axisObj.plot(datasets[dataIndex][0], datasets[dataIndex][1], label=datasetLabels[dataIndex], color=next(plotOptions["colorCycle"]), linestyle=next(plotOptions["linestyleCycle"]))
    return axisObj
