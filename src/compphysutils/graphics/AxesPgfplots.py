from Axes import Axes
from Axes import Figure

class FigurePgfplots(Figure):

    def tikzheader(self):
        return "\\begin{tikzpicture}"

    def tikzfooter(self):
        return "\\end{tikzpicture}"

    def start(self):
        print(self.tikzheader())

    def end(self):
        print(self.tikzfooter())

class AxesPgfplots(Axes):

    def axesheader(self):
        return "\\begin{axis}"
    def plotheader(self):
        return "\\addplot+[sharp plot] coordinates {"
    def plotfooter(self):
        return "};"
    def axesfooter(self):
        return "\\end{axis}"

    def start(self):
        print(self.axesheader())

    def end(self):
        print(self.axesfooter())

    def plot(self, x, y, label=False, color=False, linestyle=False):
        print(self.plotheader())
        # TODO : Color, linestyle
        for i in range(len(x)):
            # TODO : Decide on a float format
            print("({},{}) ".format(x[i], y[i]))
        # TODO : labels
        print(self.plotfooter())
