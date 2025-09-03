from Axes import Axes
from Axes import Figure

class FigurePgfplots(Figure):

    def tikzheader(self):
        return "\\begin{tikzpicture}\n"

    def tikzfooter(self):
        return "\\end{tikzpicture}\n"

    def start(self):
        return self.tikzheader()

    def end(self):
        return self.tikzfooter()

    def save(self, name):
        out = self.start()
        for ax in self.axes:
            out += ax.start()
            out += ax.buffer
            out += ax.end()
        out += self.end()
        # TODO : Lot of checks
        with open(name, "w+") as file:
            file.write(out)

class AxesPgfplots(Axes):

    def __init__(self):
        self.buffer = ""

    def axesheader(self):
        return "\\begin{axis}\n"
    def plotheader(self):
        return "\\addplot+[sharp plot] coordinates {\n"
    def plotfooter(self):
        return "};\n"
    def axesfooter(self):
        return "\\end{axis}\n"

    def start(self):
        return self.axesheader()

    def end(self):
        return self.axesfooter()

    def plot(self, x, y, label=False, color=False, linestyle=False):
        self.buffer += self.plotheader()
        # TODO : Color, linestyle
        for i in range(len(x)):
            # TODO : Decide on a float format
            self.buffer += "({},{}) ".format(x[i], y[i])
        # TODO : labels
        self.buffer += self.plotfooter()
