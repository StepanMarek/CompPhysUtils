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
        # Legend position
        if self.legend and self.legend_pos:
            # TODO: Separate position when provided
            out += ",\nlegend pos="+" ".join(map(lambda x: anchor_translator[x], self.legend_pos.split()[0:2]))
        # Legend columns
        if self.legend and self.legend_cols:
            out += ",\nlegend columns="+str(self.legend_cols)
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

    def plotheader(self, linestyle=False, color=False, markerstyle=False):
        val = "\\addplot[sharp plot"
        if linestyle:
            val += ","+linestyle
        if color:
            val += ","+color
        if markerstyle:
            val += ",mark="+markerstyle
        val += "] coordinates {\n"
        return val
    def plotfooter(self):
        return "};\n"
    def axesfooter(self):
        return "\\end{axis}\n"

    def scatterheader(self, color=False, markerstyle=False):
        val = "\\addplot[only marks"
        if color:
            val += ","+color
        if markerstyle:
            val += ",mark="+markerstyle
        val += "] coordinates {\n"
        return val

    def errorbarheader(self, color=False, markerstyle=False, linestyle=False):
        val = "\\addplot["
        if linestyle:
            val += "sharp plot"
        else:
            val += "only marks"
        if color:
            val += ","+color
        if markerstyle:
            val += ",mark="+markerstyle
        val += ",error bars/.cd"
        # TODO : More sophisticated error settings?
        val += ",y dir=both,y explicit,x dir=both,x explicit"
        val += "] coordinates {\n"
        return val

    def output_xy(self, x, y, xerr=False, xmerr=False, yerr=False, ymerr=False):
        val = ""
        if xerr and yerr and xmerr and ymerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += "({},{}) += ({},{}) -= ({},{})\n".format(x[i], y[i], xerr[i], yerr[i], xmerr[i], ymerr[i])
        elif xerr and xmerr and yerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += "({},{}) += ({},{}) -= ({},{})\n".format(x[i], y[i], xerr[i], yerr[i], xmerr[i], yerr[i])
        elif xerr and ymerr and yerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += "({},{}) += ({},{}) -= ({},{})\n".format(x[i], y[i], xerr[i], yerr[i], xerr[i], ymerr[i])
        elif xerr and yerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += "({},{}) +- ({},{})\n".format(x[i], y[i], xerr[i], yerr[i])
        elif xerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += "({},{}) +- ({},{})\n".format(x[i], y[i], xerr[i], 0)
        elif yerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += "({},{}) +- ({},{})\n".format(x[i], y[i], 0, yerr[i])
        else:
            for i in range(len(x)):
                val += "({},{})\n".format(x[i], y[i])
        return val

    def start(self):
        return self.axesheader()

    def end(self):
        return self.axesfooter()

    def plot(self, x, y, label=False, color=False, linestyle=False, markerstyle=False):
        self.buffer += self.plotheader(linestyle=linestyle, color=color, markerstyle=markerstyle)
        self.buffer += self.output_xy(x, y)
        self.buffer += self.plotfooter()
        if label:
            # TODO : Cannot separate the legend for single axis into several boxes
            # TODO : Also think about how to put legends from several axes into a single box
            self.buffer += "\\addlegendentry{"+str(label)+"}"
    
    def scatter(self, x, y, label=False, color=False, markerstyle=False, linestyle=False):
        if not linestyle:
            self.buffer += self.scatterheader(color=color, markerstyle=markerstyle)
        else:
            self.buffer += self.plotheader(linestyle=linestyle, color=color, markerstyle=markerstyle)
        self.buffer += self.output_xy(x, y)
        self.buffer += self.plotfooter()
        if label:
            self.buffer += "\\addlegendentry{"+str(label)+"}"

    def errorbar(self, x, y, xerr=False, xmerr=False, yerr=False, ymerr=False, label=False, color=False, markerstyle=False, linestyle=False):
        self.buffer += self.errorbarheader(color, markerstyle, linestyle)
        self.buffer += self.output_xy(x, y, xerr=xerr, xmerr=xmerr, yerr=yerr, ymerr=ymerr)
        self.buffer += self.plotfooter()
        if label:
            self.buffer += "\\addlegendentry{"+str(label)+"}"

    def colormap(self, x, y, c, label=False, cmap=False):
        """
        Already created the mesh x y c
        """
        # TODO : Cmap, label
        self.buffer += "\\addplot[patch,patch type=rectangle,shader=interp,point meta=explicit] coordinates {\n"
        for i in range(len(x)-1):
            for j in range(len(x[0])-1):
                self.buffer += "({},{}) [{}]\n".format(x[i][j],y[i][j],c[i][j])
                self.buffer += "({},{}) [{}]\n".format(x[i+1][j],y[i+1][j],c[i+1][j])
                self.buffer += "({},{}) [{}]\n".format(x[i+1][j+1],y[i+1][j+1],c[i+1][j+1])
                self.buffer += "({},{}) [{}]\n".format(x[i][j+1],y[i][j+1],c[i][j+1])
        self.buffer += "};\n"
