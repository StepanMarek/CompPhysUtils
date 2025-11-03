class Figure():

    # List of axes present in this figure
    
    def __init__(self):
        # TODO : Design API for axes positioning
        self.axes = []
        # List of export formats supported by the backend
        self.allowed_formats = []
        # Default dimensions - in cm - ratio 4/3
        self.width = 16
        self.height = 12

    def start(self):
        raise NotImplementedError("Start function for figure not implemented")

    def end(self):
        raise NotImplementedError("End function for figure not implemented")

    def save(self, name):
        """
        Write out the figure to a file.
        Extension should be determined by allowed_formats.
        """
        raise NotImplementedError("Save not implemented in this backend")

class Axes():

    def __init__(self):
        self.xlim = False
        self.ylim = False

        self.xticks = False
        self.xtick_labels = False
        self.xticks_swap = False
        self.xticks_rotate = 0.0
        self.yticks = False
        self.ytick_labels = False
        self.yticks_swap = False
        self.yticks_rotate = 0.0

        # Can be set to "x", "y", "both" or False
        # TODO : Make an enum?
        self.hide_axes = False

        self.xscale = "lin"
        self.yscale = "lin"

        # width of the x/y axis
        self.axes_width = 1.0

        # Axes labels
        self.labels = [False,False]

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

    def colormap(self, x, y, c, label=False, cmap=False):
        """
        Colormap, using already mesh of x y c (two dimensional)
        """
        raise NotImplementedError("Colormap not implemented in this backend")

    def inset_axes(self, x, y, width, height):
        """
        Create the inset axes object
        """
        raise NotImplementedError("Insets not implemented in this backend")
