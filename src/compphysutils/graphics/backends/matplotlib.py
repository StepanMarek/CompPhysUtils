from compphysutils.graphics import Figure as FigureBase, Axes as AxesBase
import matplotlib

class Figure(FigureBase):
    def __init__(self):
        super().__init__()
        self.allowed_formats.append("png")
        self.allowed_formats.append("pdf")
        self.allowed_formats.append("svg")
        self._figure = matplotlib.figure.Figure()

    def save(self, name):
        self._figure.savefig(name)

class Axes(AxesBase):
    def __init__(self, figure):
        super().__init__(figure)
        self._axes = figure._figure.add_axes((0.0, 0.0, 1.0, 1.0))

    def plot(self, x, y, label=False, color=False, linestyle=False):
        self._axes.plot(x, y, label=label, color=color, linestyle=linestyle)
