from .Vector import Vector
import array

class VectorReal(Vector):
    """
    Implements the vector for real numbers, storing the components as fixed length array of floats
    """

    def __init__(self, *args):
        self.components = array.array("f", [0,0,0])
        for i in range(len(args)):
            self.components[i] = args[i]
