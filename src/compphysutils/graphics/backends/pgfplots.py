from compphysutils.graphics import Figure as FigureBase, Axes as AxesBase

anchor_translator = {
    "upper" : "north",
    "lower" : "south",
    "right" : "east",
    "left" : "west"
}

class Figure(FigureBase):

    def __init__(self):
        super().__init__()
        self.allowed_formats.append("pgf")
        # TODO - tex format - standalone, compilable tex
        # TODO - pdf format - when pdflatex/other tex engine is present, compile with it?

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
            # TODO : Redo via headers API
            # out += ax.start(width=self.width, height=self.height)
            out += ax.start()
            out += ax.buffer
            out += ax.end()
        out += self.end()
        # TODO : Lot of checks
        with open(name, "w+") as file:
            file.write(out)

class Axes(AxesBase):

    def __init__(self):
        super().__init__()
        self.buffer = ""
        self.legend_entries = False
        # Primitive headers - key is an identifier of the header, value can be either
        # None or some value - in case of None, the header key is output without value
        self.headers = {}
        self.plot_headers = {}
        self.inset_id = 0

    def add_header(self, header, value=None):
        self.headers[header] = value

    def add_plot_header(self, header, value=None):
        self.plot_headers[header] = value

    def get_header_string(self, headers):
        header_strings = []
        for header in headers:
            if headers[header] != None:
                header_string = str(header)+"="+str(headers[header])
            else:
                header_string = str(header)
            header_strings.append(header_string)
        return ",\n".join(header_strings)

    def axesheader(self, width="\\columnwidth", height=False):
        # Axes size
        if width:
            if type(width) == float or type(width) == int:
                self.add_header("width", str(width)+"cm")
            else:
                self.add_header("width", str(width))
        if height:
            if type(height) == float or type(height) == int:
                self.add_header("height", str(height)+"cm")
            else:
                self.add_header("height", str(height))
        # Hide axes
        if self.hide_axes == "both":
            self.add_header("axis lines", "none")
        elif self.hide_axes == "x":
            self.add_header("axis x line", "none")
        elif self.hide_axes == "y":
            self.add_header("axis y line", "none")
        # Axes labels
        if self.labels[0]:
            self.add_header("xlabel", self.labels[0])
        if self.labels[1]:
            self.add_header("ylabel", self.labels[1])
        # Limits
        if self.xlim:
            if self.xlim[0] or type(self.xlim[0]) != bool:
                self.add_header("xmin", self.xlim[0])
            if self.xlim[1] or type(self.xlim[1]) != bool:
                self.add_header("xmax", self.xlim[1])
        if self.ylim:
            if self.ylim[0] or type(self.ylim[0]) != bool:
                self.add_header("ymin", self.xlim[0])
            if self.ylim[1] or type(self.ylim[1]) != bool:
                self.add_header("ymax", self.xlim[1])
        # Legend position
        if self.legend and self.legend_pos:
            # TODO: Separate position when provided
            self.add_header("legend pos", " ".join(map(lambda x: anchor_translator[x], self.legend_pos.split()[0:2])))
        # Legend columns
        if self.legend and self.legend_cols:
            self.add_header("legend columns", self.legend_cols)
        # Tick axis positions
        if self.xticks_swap:
            self.add_header("xticklabel pos", "upper")
        if self.yticks_swap:
            self.add_header("yticklabel pos", "upper")
        # Tick positions
        if self.xticks:
            # TODO : Tick pos float formatting?
            self.add_header("xtick", "{"+",".join(map(str, self.xticks))+"}")
        if self.yticks:
            # TODO : Tick pos float formatting?
            self.add_header("ytick", "{"+",".join(map(str, self.yticks))+"}")
        # Tick labels
        if self.xtick_labels:
            self.add_header("xticklabels", "{"+",".join(map(str, self.xtick_labels))+"}")
        if self.ytick_labels:
            self.add_header("yticklabels", "{"+",".join(map(str, self.ytick_labels))+"}")
        # Tick label rotation
        if self.xticks_rotate:
            self.add_header("x tick label style", "{rotate="+str(self.xticks_rotate)+"}")
        if self.yticks_rotate:
            self.add_header("y tick label style", "{rotate="+str(self.yticks_rotate)+"}")
        return "\\begin{axis}[" + self.get_header_string(self.headers) + "\n]\n"

    def generic_plot_headers(self, linestyle=False, color=False, markerstyle=False):
        # TODO : Typechecks?
        if linestyle:
            self.add_plot_header(linestyle)
        if color:
            self.add_plot_header(color)
        if markerstyle:
            self.add_plot_header("mark", markerstyle)
        return "\\addplot[" + self.get_header_string(self.plot_headers) + "\n] coordinates {\n"

    def plotheader(self, linestyle=False, color=False, markerstyle=False):
        self.add_plot_header("sharp plot")
        return self.generic_plot_headers(linestyle, color, markerstyle)

    def plotfooter(self):
        return "};\n"

    def axesfooter(self):
        return "\\end{axis}\n"

    def scatterheader(self, color=False, markerstyle=False):
        self.add_plot_header("only marks")
        return self.generic_plot_headers(color=color, markerstyle=markerstyle)

    def errorbarheader(self, color=False, markerstyle=False, linestyle=False):
        if linestyle:
            self.add_plot_header("sharp plot")
        else:
            self.add_plot_header("only marks")
        self.add_plot_header("error bars/.cd")
        # TODO : More sophisticated error settings?
        self.add_plot_header("y dir", "both")
        self.add_plot_header("y explicit")
        self.add_plot_header("x dir", "both")
        self.add_plot_header("x explicit")
        return self.generic_plot_headers(linestyle=linestyle, color=color, markerstyle=markerstyle)
        # val = "\\addplot["
        # if linestyle:
        #     val += "sharp plot"
        # else:
        #     val += "only marks"
        # if color:
        #     val += ","+color
        # if markerstyle:
        #     val += ",mark="+markerstyle
        # val += ",error bars/.cd"
        # # TODO : More sophisticated error settings?
        # val += ",y dir=both,y explicit,x dir=both,x explicit"
        # val += "] coordinates {\n"
        # return val

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

    def start(self, width=16, height=12):
        return self.axesheader(width, height)

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
        self.add_plot_header("patch")
        self.add_plot_header("patch type", "rectangle")
        self.add_plot_header("shader", "interp")
        self.add_plot_header("point meta", "explicit")
        self.buffer += self.generic_plot_headers()
        #self.buffer += "\\addplot[patch,patch type=rectangle,shader=interp,point meta=explicit] coordinates {\n"
        for i in range(len(x)-1):
            for j in range(len(x[0])-1):
                self.buffer += "({},{}) [{}]\n".format(x[i][j],y[i][j],c[i][j])
                self.buffer += "({},{}) [{}]\n".format(x[i+1][j],y[i+1][j],c[i+1][j])
                self.buffer += "({},{}) [{}]\n".format(x[i+1][j+1],y[i+1][j+1],c[i+1][j+1])
                self.buffer += "({},{}) [{}]\n".format(x[i][j+1],y[i][j+1],c[i][j+1])
        self.buffer += "};\n"

    def inset_axes(self, x, y, width, height):
        """
        Create the inset axes object
         - add coordinate reference to this axes
         - add at header to the new axes
        """
        new_axes = Axes()
        self.buffer += "\\coordinate (insetref"+str(self.inset_id)") at (rel axis cs: "+str(x)+","+str(y)+");"
        new_axes.add_header("at", "{(insetref"+str(self.inset_id)+")}")
        new_axes.add_header("width", self.headers["width"]*width)
        new_axes.add_header("height", self.headers["height"]*height)
        self.inset_id += 1;
        return new_axes
        
