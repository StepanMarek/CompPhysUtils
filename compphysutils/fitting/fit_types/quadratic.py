def fit(x, curvature, centre, offset):
    return curvature*((x - centre) ** 2) + offset

def guess(datasetX, datasetY):
    # Assume approximately centered
    centre = (datasetX[-1] + datasetX[0]) * 0.5
    offset = min(datasetY)
    # Find max index of y
    maxY = offset
    imaxY = 0
    for i in range(len(datasetY)):
        if datasetY[i] > maxY:
            maxY = datasetY[i]
            imaxY = i
    maxX = datasetX[imaxY]
    curvature = (maxY - offset) / ((maxX - centre) ** 2)
    return curvature, centre, offset
paramNames = ["Curvature", "Centre", "Offset"]
