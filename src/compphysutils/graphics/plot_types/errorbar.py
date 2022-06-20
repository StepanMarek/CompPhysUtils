def plot(datasets, axisObj, datasetLabels=False, **plotOptions):
    if not datasetLabels:
        datasetLabels = [None] * len(datasets)
    for dataIndex in range(len(datasets)):
        if len(datasets[dataIndex]) >= 4:
            # If at least four columns provided, plot errors on both axes
            axisObj.errorbar(datasets[dataIndex][0], datasets[dataIndex][2], xerr=datasets[dataIndex][1], yerr=datasets[dataIndex][3], capsize=4, lw=0, elinewidth=2, marker="p", ms=1, label=datasetLabels[dataIndex], color=next(plotOptions["colorCycle"]))
        else:
            # Otherwise, just plot yerr
            axisObj.errorbar(datasets[dataIndex][0], datasets[dataIndex][1], yerr=datasets[dataIndex][2], capsize=4, lw=0, elinewidth=2, marker="p", ms=2, label=datasetLabels[dataIndex], color=next(plotOptions["colorCycle"]))
    return axisObj
