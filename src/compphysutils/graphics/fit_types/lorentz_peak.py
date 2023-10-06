import math

def fit(x, centre, damping, amplitude):
    return amplitude/((x - centre) ** 2 + damping ** 2)

def guess(datasetX, datasetY):
    # Use the position of max of abs(y)
    maxY = max(datasetY)
    minY = min(datasetY)
    targetY = maxY
    if abs(minY) > abs(maxY):
        # Use minY
        targetY = minY
    centreIndex = datasetY.index(targetY)
    centre = datasetX[centreIndex]
    amplitude = (datasetX[centreIndex-1] - datasetX[centreIndex]) ** 2 / (1/datasetY[centreIndex-1] - 1/datasetY[centreIndex])
    damping = (amplitude / targetY) ** 0.5
    return centre, damping, amplitude

paramNames = ["Centre", "Damping", "Amplitude"]
