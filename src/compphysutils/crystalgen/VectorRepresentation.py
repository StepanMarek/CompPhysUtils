from .Vector import Vector
import array

class VectorRepresentation(Vector):
    """
    Implements the vector representation by using fixed length array of int only
    """

    def __init__(self, *args):
        self.components = array.array("i", [0,0,0])
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
