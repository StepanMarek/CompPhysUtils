class Vector:
    """
    Implements the basic setting and getting of components, scalar products, scalar multiplication and addition
    """

    def val_getter(self, valIndex):
        return self.components[valIndex]

    def val_setter(self, valIndex, val):
        self.components[valIndex] = val
        return self.components[valIndex]

    def val_deleter(self, valIndex):
        del self.components[valIndex]

    x = property(lambda self: self.val_getter(0),lambda self, val: self.val_setter(0, val), lambda self: self.val_deleter(0))
    y = property(lambda self: self.val_getter(1),lambda self, val: self.val_setter(1, val), lambda self: self.val_deleter(1))
    z = property(lambda self: self.val_getter(2),lambda self, val: self.val_setter(2, val), lambda self: self.val_deleter(2))

    def __init__(self, *args):
        if len(args) >= 3:
            self.components = [0]*len(args)
        else:
            self.components = [0,0,0]
        for i in range(len(args)):
            self.components[i] = args[i]

    def __str__(self):
        return "("+",".join(map(str, self.components))+")"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if issubclass(type(other), Vector):
            return type(self)(*map(lambda x: x[0]+x[1], zip(self.components, other.components)))
        else:
            raise TypeError("Addition not implemented for "+str(type(self))+" and "+str(type(other)))

    def __sub__(self, other):
        if issubclass(type(other), Vector):
            return type(self)(*map(lambda x: x[0]-x[1], zip(self.components, other.components)))
        else:
            raise TypeError("Subtraction not implemented for "+str(type(self))+" and "+str(type(other)))

    def __mul__(self, other):
        if issubclass(type(other), Vector):
            # Scalar (dot) product
            return sum(*map(lambda comps: comps[0]*comps[1], zip(self.components, other.components)))
        else:
            # Asume scalar multiplication
            res = type(self)(*map(lambda x: other * x, self.components))
            return res

    def __rmul__(self, other):
        # Multiplication is always symmetric
        return self.__mul__(other)

    def __neg__(self):
        # Only return scalar multiple
        return (-1) * self

    def __abs__(self):
        # Returns magnitude of the vector
        return (sum(map(lambda x:x**2, self.components)))**0.5

    def cloneZeros(self):
        return type(self)(*([0]*len(self.components)))
