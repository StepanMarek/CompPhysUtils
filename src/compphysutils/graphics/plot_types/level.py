def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        # For x positions, only takes into account first element
        axisObj.eventplot(datasets[dataIndex][1], lineoffsets=datasets[dataIndex][0][0], orientation="vertical", label=datasetLabels[dataIndex], colors=next(plotOptions["colorCycle"]))
    return axisObj
