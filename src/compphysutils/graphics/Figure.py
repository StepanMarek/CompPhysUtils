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
        self.xlim = False
        self.ylim = False

        self.xticks = False
        self.xtick_labels = False
        self.xtick_swap = False
        self.yticks = False
        self.ytick_labels = False
        self.ytick_swap = False

        self.xscale = "lin"
        self.yscale = "lin"

        # width of the x/y axis
        self.axes_width = 1.0

        # Axes labels
        self.labels = ["",""]

        # Show/hide legend
        self.legend = True

        # Legend position
        self.legend_pos = False

        # Number of legend columns
        self.legend_cols = 1

    def plot(self, x, y, label=False, color=False, linestyle=False):
        """
        Adds a new dataset to the axes and plots it as a line graph.
        Should be stored in an internal buffer
        and only written out on save/show called from the figure controlling figure

        label here stands for dataset label for the legend
        """
        raise NotImplementedError("Plot not implemented in this backend")

    def scatter(self, x, y, label=False, color=False, markerstyle=False, linestyle=False):
        """
        Similar to plot, but uses scatter graph instead of the line graph, optionally connects
        the scatter points by a line.
        """
        raise NotImplementedError("Scatter not implemented in this backend")

    def errorbar(self, x, y, xerr=False, yerr=False, label=False, color=False, markerstyle=False, linestyle=False):
        """
        Extension of the scatter plot to include (so far) symmetric error bars
        """
        raise NotImplementedError("Errorbar not implemented in this backend")
