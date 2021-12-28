from .Vector import Vector
import array

class VectorRepresentation(Vector):
    """
    Implements the vector representation by using fixed length array of int only
    """

    def __init__(self, *args):
        if len(args) < 3:
            self.components = array.array("i", [0,0,0])
        else:
            self.components = array.array("i", [0]*len(args))
        for i in range(len(args)):
            self.components[i] = args[i]

    def __eq__(self, other):
        """
        Importantly, vector representation implements the exact equals method, as this is necessary to eliminate numerical noise in float positions
        """
        if type(other) == VectorRepresentation:
            isEqual = True
            for i in range(len(self.components)):
                isEqual = isEqual and (self.components[i] == other.components[i])
            return isEqual
        else:
            raise TypeError("Equivalence relation unknown for VectorRepresentation and "+str(type(other)))

    def translateToBasis(self, basis):
        if len(basis) != len(self.components):
            #raise ArithmeticError("The basis size "+str(len(basis))+" and the vector size "+str(len(self.components))" are different!")
            raise ArithmeticError("Different basis and vector size!")
        return sum(map(lambda x: x[0] * x[1], zip(self.components, basis)), basis[0].cloneZeros())

