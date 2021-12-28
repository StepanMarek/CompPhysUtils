from .Vector import Vector
import array

class VectorReal(Vector):
    """
    Implements the vector for real numbers, storing the components as fixed length array of floats
    """

    def __init__(self, *args):
        if len(args) < 3:
            self.components = array.array("f", [0]*3)
        else:
            self.components = array.array("f", [0]*len(args))
        for i in range(len(args)):
            self.components[i] = args[i]
