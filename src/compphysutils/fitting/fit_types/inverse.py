def fit(x, constant):
    return constant/x

def guess(datasetX, datasetY):
    # Guess as mean
    sumGuesses = 0
    for i in range(len(datasetX)):
        sumGuesses += datasetY[i] * datasetX[i]
    return sumGuesses / len(datasetX)
paramNames = ["Constant"]
