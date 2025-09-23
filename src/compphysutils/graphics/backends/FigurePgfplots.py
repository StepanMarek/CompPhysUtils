from ..Figure import Figure
from ..Figure import Axes

anchor_translator = {
    "upper" : "north",
    "lower" : "south",
    "right" : "east",
    "left" : "west"
}

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
        super().__init__()
        self.buffer = ""
        self.legend_entries = False

    def axesheader(self):
        out = "\\begin{axis}["
        # Axis labels
        if self.labels:
            if self.labels[0]:
                out += "\nxlabel={"+self.labels[0]+"}"
            if self.labels[1]:
                out += ",\nylabel={"+self.labels[1]+"}"
        # Limits
        if self.xlim:
            if self.xlim[0] or type(self.xlim[0]) != bool:
                out += ",\nxmin="+str(self.xlim[0])
            if self.xlim[1] or type(self.xlim[1]) != bool:
                out += ",\nxmax="+str(self.xlim[1])
        if self.ylim:
            if self.ylim[0] or type(self.ylim[0]) != bool:
                out += ",\nymin="+str(self.ylim[0])
            if self.ylim[1] or type(self.ylim[1]) != bool:
                out += ",\nymax="+str(self.ylim[1])
        # Legend entries
        if self.legend and self.legend_entries:
            out += ",\nlegend entries={"+",".join(self.legend_entries)+"}"
        # Legend position
        if self.legend_pos:
            # TODO: Separate position when provided
            out += ",\nlegend pos="+" ".join(map(lambda x: anchor_translator[x], self.legend_pos.split()[0:2]))
        # Tick axis positions
        if self.xtick_swap:
            out += ",\nxticklabel pos=upper"
        if self.ytick_swap:
            out += ",\nyticklabel pos=upper"
        # Tick positions
        if self.xticks:
            # TODO : Tick pos float formatting?
            out += ",\nxtick={"+",".join(map(str, self.xticks))+"}"
        if self.yticks:
            # TODO : Tick pos float formatting?
            out += ",\nytick={"+",".join(map(str, self.yticks))+"}"
        # Tick labels
        if self.xtick_labels:
            out += ",\nxticklabels={"+",".join(self.xtick_labels)+"}"
        if self.ytick_labels:
            out += ",\nyticklabels={"+",".join(self.ytick_labels)+"}"
        out += "\n]\n"
        return out

    def plotheader(self, linestyle=False, color=False):
        val = "\\addplot[sharp plot"
        if linestyle:
            val += ","+linestyle
        if color:
            val += ","+color
        val += "] coordinates {\n"
        return val
    def plotfooter(self):
        return "};\n"
    def axesfooter(self):
        return "\\end{axis}\n"

    def start(self):
        return self.axesheader()

    def end(self):
        return self.axesfooter()

    def plot(self, x, y, label=False, color=False, linestyle=False):
        if label:
            if self.legend_entries:
                self.legend_entries.append(label)
            else:
                self.legend_entries = [label]
        self.buffer += self.plotheader(linestyle=linestyle, color=color)
        # TODO : Color, linestyle
        for i in range(len(x)):
            # TODO : Decide on a float format
            self.buffer += "({},{}) ".format(x[i], y[i])
        # TODO : labels
        self.buffer += self.plotfooter()
