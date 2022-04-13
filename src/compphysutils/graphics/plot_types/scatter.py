def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        axisObj.scatter(datasets[dataIndex][0], datasets[dataIndex][1], label=datasetLabels[dataIndex], c=next(plotOptions["colorCycle"]))
    return axisObj
