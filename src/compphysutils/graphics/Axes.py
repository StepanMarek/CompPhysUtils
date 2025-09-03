class Figure():

    # List of axes present in this figure
    
    def __init__(self):
        # TODO : Design API for axes positioning
        self.axes = []

    def start(self):
        raise NotImplementedError("Start function for figure not implemented")

    def end(self):
        raise NotImplementedError("End function for figure not implemented")

    def save(self, name):
        """
        Write out the figure to a file.
        """
        raise NotImplementedError("Save not implemented in this backend")

class Axes():

    def __init__(self):
        self.xlabel = "x"
        self.ylabel = "y"
        self.xlim = [0,1]
        self.ylim = [0,1]

        self.xticks = False
        self.yticks = False

        self.xscale = "lin"
        self.yscale = "lin"

        # width of the x/y axis
        self.axes_width = 1.0

        self.labels = []

    def plot(self, x, y, label=False, color=False, linestyle=False):
        """
        Adds a new dataset to the axes. Should be stored in an internal buffer
        and only written out on save/show called from the figure controlling figure
        """
        raise NotImplementedError("Plot not implemented in this backend")
