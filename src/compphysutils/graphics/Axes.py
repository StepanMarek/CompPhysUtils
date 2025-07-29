class Figure():

    def start(self):
        raise NotImplementedError("Start function for figure not implemented")

    def end(self):
        raise NotImplementedError("End function for figure not implemented")

class Axes():
    xlabel = "x"
    ylabel = "y"
    xlim = [0,1]
    ylim = [0,1]

    xticks = False
    yticks = False

    xscale = "lin"
    yscale = "lin"

    # width of the x/y axis
    axes_width = 1.0

    labels = []

    def plot(self, x, y, label=False, color=False, linestyle=False):
        raise NotImplementedError("Plot not implemented in this backend")
