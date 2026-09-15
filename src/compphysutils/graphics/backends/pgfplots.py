from compphysutils.graphics import Figure as FigureBase, Axes as AxesBase

anchor_translator = {
    "upper left" : "north west",
    "upper center" : "north",
    "upper right" : "north east",
    "center left" : "west",
    "center" : "base",
    "center right" : "east",
    "lower left" : "south west",
    "lower center" : "south",
    "lower right" : "south east"
}
coord_translator = {
    "upper left" : (0.05,0.95),
    "upper center" : (0.5,0.95),
    "upper right" : (0.95,0.95),
    "center left" : (0.05,0.5),
    "center" : (0.5,0.5),
    "center right" : (0.95,0.5),
    "lower left" : (0.05,0.05),
    "lower center" : (0.5,0.05),
    "lower right" : (0.95,0.05)
}

float_format="{:12.4E}"
"""
Standardizes float output format
"""

transform_cs = {
        "axes" : "rel axis cs",
        "data" : "axis cs"
}
"""
Standard coord transforms
"""

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

    def __init__(self, figure):
        super().__init__(figure)
        self.buffer = ""
        self.legend_entries = False
        # Primitive headers - key is an identifier of the header, value can be either
        # None or some value - in case of None, the header key is output without value
        self.headers = {}
        self.plot_headers = {}
        self.extra_xtick_coords = []
        self.extra_ytick_coords = []
        self.inset_id = 0
        # Loading of extra tikz libs
        self.extra_libs = []
        figure.axes.append(self)

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

    def axesheader(self):
        # Axes size
        if type(self.width) == float or type(self.width) == int:
            self.add_header("width", str(self.width)+"cm")
        else:
            self.add_header("width", str(self.width))
        if type(self.height) == float or type(self.height) == int:
            self.add_header("height", str(self.height)+"cm")
        else:
            self.add_header("height", str(self.height))
        # Hide axes
        if self.hide_axes == "both":
            self.add_header("axis lines", "none")
        elif self.hide_axes == "x":
            self.add_header("axis x line", "none")
        elif self.hide_axes == "y":
            self.add_header("axis y line", "none")
        # Axes labels
        if self.labels[0]:
            # TODO : labelPos needed or not?
            # if self.labelPos[0]:
            #     self.add_header("xlabel style={align="+self.labelPos[0]+"}", self.labels[0])
            # else:
            #     self.add_header("xlabel", self.labels[0])
            self.add_header("xlabel", self.labels[0])
        if self.labels[1]:
            # if self.labelPos[1]:
            #     self.add_header("ylabel style={align="+self.labelPos[1]+"}", self.labels[1])
            # else:
            #     self.add_header("ylabel", self.labels[1])
            self.add_header("ylabel", self.labels[1])
        # Limits
        if self.xlim:
            if self.xlim[0] or type(self.xlim[0]) != bool:
                self.add_header("xmin", self.xlim[0])
            if self.xlim[1] or type(self.xlim[1]) != bool:
                self.add_header("xmax", self.xlim[1])
        if self.ylim:
            if self.ylim[0] or type(self.ylim[0]) != bool:
                self.add_header("ymin", self.ylim[0])
            if self.ylim[1] or type(self.ylim[1]) != bool:
                self.add_header("ymax", self.ylim[1])
        # Legend position
        if self.legend and self.legend_pos:
            # TODO: Separate position when provided
            pos_args = self.legend_pos.split()
            # First two arguments need to be translated to anchor
            # If only one argument given
            anchor = "base"
            coords = [0.5, 0.5]
            if len(pos_args) == 1:
                # Only one option, but run through the translator for completeness
                anchor = anchor_translator[pos_args[0]]
            elif len(pos_args) == 2:
                # Must be description without coordinates
                basename = " ".join(pos_args) 
                anchor = anchor_translator[basename]
                # Depending on the anchor, determine the coords
                coords = coord_translator[basename]
            elif len(pos_args) == 3:
                # Must be center + coords
                anchor = anchor_translator[pos_args[0]]
                coords[0] = float(pos_args[1])
                coords[1] = float(pos_args[2])
            else:
                # Full spec
                anchor = " ".join(pos_args[0:2])
                anchor = anchor_translator[anchor]
                coords[0] = float(pos_args[2])
                coords[1] = float(pos_args[3])
            self.add_header("legend style", "{at={("+",".join(map(str, coords))+")},anchor="+anchor+"}")
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
        # axes linewidth
        if self.axes_linewidth:
            self.add_header("line width", str(self.axes_linewidth)+"pt")
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
        # Extra ticks
        if len(self.extra_xtick_coords) > 0:
            coordlist = ",".join(map(lambda x: float_format.format(x), self.extra_xtick_coords))
            self.add_header("extra x ticks", "{"+coordlist+"}")
        if len(self.extra_ytick_coords) > 0:
            coordlist = ",".join(map(lambda x: float_format.format(x), self.extra_ytick_coords))
            self.add_header("extra y ticks", "{"+coordlist+"}")
        # Extra libs
        extra_libs = ",".join(self.extra_libs)
        output = r"\usetikzlibrary{"+extra_libs+"}\n"
        return output+"\\begin{axis}[" + self.get_header_string(self.headers) + "\n]\n"

    def set_yscale(self, mode="linear", base=False):
        self.add_header("ymode", mode)
        if base:
            self.add_header("log basis y", str(base))

    def set_xscale(self, mode="linear", base=False):
        self.add_header("xmode", mode)
        if base:
            self.add_header("log basis x", str(base))

    def generic_plot_headers(self, linestyle=False, color=False, markerstyle=False, linewidth=False):
        # TODO : Typechecks?
        if linestyle:
            self.add_plot_header(linestyle)
        if color:
            self.add_plot_header(color)
        if markerstyle:
            self.add_plot_header("mark", markerstyle)
        if not (type(linewidth) == bool and (not linewidth)):
            self.add_plot_header("line width", str(linewidth)+"pt")
        return "\\addplot[" + self.get_header_string(self.plot_headers) + "\n] coordinates {\n"

    def plotheader(self, linestyle=False, color=False, markerstyle=False):
        self.add_plot_header("sharp plot")
        return self.generic_plot_headers(linestyle, color, markerstyle)

    def plotfooter(self):
        return "};\n"

    def axesfooter(self):
        return "\\end{axis}\n"

    def errorbarheader(self, color=False, markerstyle=False, linestyle=False, elinewidth=False, capsize=False, linewidth=0):
        if linestyle or linewidth:
            self.add_plot_header("sharp plot")
        else:
            self.add_plot_header("only marks")
            # In this case, set line width to default line width, for good rendering of line-markers
            linewidth=1
        # Due to peculiar syntax, generic headers must be placed before error bar headers
        if linestyle:
            self.add_plot_header(linestyle)
        if color:
            self.add_plot_header(color)
        if markerstyle:
            self.add_plot_header("mark", markerstyle)
        if not (type(linewidth) == bool and (not linewidth)):
            self.add_plot_header("line width", str(linewidth)+"pt")
        self.add_plot_header("error bars/.cd")
        self.add_plot_header("y dir", "both")
        self.add_plot_header("y explicit")
        self.add_plot_header("x dir", "both")
        self.add_plot_header("x explicit")
        if not (type(elinewidth) == bool and (not elinewidth)):
            self.add_plot_header("error bar style", "{line width="+str(elinewidth)+"pt}")
        if not (type(capsize) == bool and (not capsize)):
            # Has to include default rotation
            opts = ["rotate=90", "mark size="+str(capsize)]
            if not (type(elinewidth) == bool and (not elinewidth)):
                opts.append("line width="+str(elinewidth)+"pt")
            self.add_plot_header("error mark options", "{"+",".join(opts)+"}")
        return "\\addplot[" + self.get_header_string(self.plot_headers) +"\n] coordinates {\n"

    def output_xy(self, x, y, xerr=False, xmerr=False, yerr=False, ymerr=False):
        val = ""
        if xerr and yerr and xmerr and ymerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += ("("+float_format+","+float_format+") += ("+float_format+","+float_format+") -= ("+float_format+","+float_format+")\n").format(x[i], y[i], xerr[i], yerr[i], xmerr[i], ymerr[i])
        elif xerr and xmerr and yerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += ("("+float_format+","+float_format+") += ("+float_format+","+float_format+") -= ("+float_format+","+float_format+")\n").format(x[i], y[i], xerr[i], yerr[i], xmerr[i], yerr[i])
        elif xerr and ymerr and yerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += ("("+float_format+","+float_format+") += ("+float_format+","+float_format+") -= ("+float_format+","+float_format+")\n").format(x[i], y[i], xerr[i], yerr[i], xerr[i], ymerr[i])
        elif xerr and yerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += ("("+float_format+","+float_format+") +- ("+float_format+","+float_format+")\n").format(x[i], y[i], xerr[i], yerr[i])
        elif xerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += ("("+float_format+","+float_format+") +- ("+float_format+","+float_format+")\n").format(x[i], y[i], xerr[i], 0)
        elif yerr:
            for i in range(len(x)):
                # TODO : Decide on a float format
                val += ("("+float_format+","+float_format+") +- ("+float_format+","+float_format+")\n").format(x[i], y[i], 0, yerr[i])
        else:
            for i in range(len(x)):
                val += ("("+float_format+","+float_format+")\n").format(x[i], y[i])
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
    
    def scatter(self, x, y, label=False, color=False, markerstyle=False, linestyle=False, markersize=False):
        self.add_plot_header("only marks")
        if markersize:
            self.add_plot_header("mark size", markersize)
        if not linestyle:
            self.buffer += self.generic_plot_headers(color=color, markerstyle=markerstyle)
        else:
            self.buffer += self.plotheader(linestyle=linestyle, color=color, markerstyle=markerstyle)
        self.buffer += self.output_xy(x, y)
        self.buffer += self.plotfooter()
        if label:
            self.buffer += "\\addlegendentry{"+str(label)+"}"

    def errorbar(self, x, y, xerr=False, xmerr=False, yerr=False, ymerr=False, label=False, color=False, markerstyle=False, linestyle=False,
                 elinewidth=2, capsize=4, linewidth=0):
        self.buffer += self.errorbarheader(color, markerstyle, linestyle, elinewidth=elinewidth, capsize=capsize, linewidth=linewidth)
        self.buffer += self.output_xy(x, y, xerr=xerr, xmerr=xmerr, yerr=yerr, ymerr=ymerr)
        self.buffer += self.plotfooter()
        if label:
            self.buffer += "\\addlegendentry{"+str(label)+"}"

    def colormap(self, x, y, c, label=False, cmap=False, vmin=False, vmax=False, norm=False, refines=0):
        """
        Already created the mesh x y c
        """
        # TODO : Cmap, label
        self.add_plot_header("patch")
        self.add_plot_header("patch type", "rectangle")
        self.add_plot_header("shader", "interp")
        self.add_plot_header("point meta", "explicit")
        self.add_plot_header("patch refines", str(refines))
        self.buffer += self.generic_plot_headers()
        # Assumes already shaped xyc mesh data
        for i in range(len(x)-1):
            for j in range(len(x[0])-1):
                self.buffer += ("("+float_format+","+float_format+") ["+float_format+"]\n").format(x[i][j],y[i][j],c[i][j])
                self.buffer += ("("+float_format+","+float_format+") ["+float_format+"]\n").format(x[i+1][j],y[i+1][j],c[i+1][j])
                self.buffer += ("("+float_format+","+float_format+") ["+float_format+"]\n").format(x[i+1][j+1],y[i+1][j+1],c[i+1][j+1])
                self.buffer += ("("+float_format+","+float_format+") ["+float_format+"]\n").format(x[i][j+1],y[i][j+1],c[i][j+1])
        self.buffer += "};\n"

    def level(self, xs, lineoffset=0, linelength=1.0, orientation="vertical", label=False, color=False, linestyle=False):
        """
        Creates the line graph -- only connection of draw lines, without \\addplot option
        """
        drawfinal = self.generic_plot_headers(linestyle=linestyle, color=color)
        self.add_plot_header("forget plot")
        drawcommand = self.generic_plot_headers(linestyle=linestyle, color=color)
        # TODO : Vertical vs horizontal
        for ix in range(len(xs)-1):
            self.buffer += drawcommand + self.output_xy([lineoffset-linelength/2,lineoffset+linelength/2], [xs[ix], xs[ix]])
            self.buffer += "};\n"
        if len(xs) > 0:
            # Only adding the legend to the last plot
            if label:
                self.buffer += drawfinal + self.output_xy([lineoffset-linelength/2,lineoffset+linelength/2], [xs[-1], xs[-1]])
                self.buffer += "};\n"
                self.buffer += "\\addlegendentry{"+str(label)+"}"
            else:
                self.buffer += drawcommand + self.output_xy([lineoffset-linelength/2,lineoffset+linelength/2], [x[ix], x[ix]])
                self.buffer += "};\n"
        # Clear headers
        self.plot_headers = {}

    def quiver(self, x, y, u, v, label=False, color=False):
        """
        Quiver graph
        """
        self.add_plot_header("quiver", "{u=\\thisrow{u},\nv=\\thisrow{v}}")
        self.add_plot_header("-stealth")
        if color:
            self.add_plot_header(color)
        # TODO : Different headers
        # self.buffer += self.generic_plot_headers(color=color)
        self.buffer +="\\addplot[" + self.get_header_string(self.plot_headers) + "\n] table {\n" 
        self.buffer += "x y u v\n"
        for i in range(len(x)):
            self.buffer += (float_format*4).format(x[i], y[i], u[i], v[i])
            self.buffer += "\n"
        self.buffer += "};\n"
        if label:
            self.buffer += r"\addlegendentry{"+str(label)+"}\n"

    def fill_between(self, x, low, high, color=False, label=False):
        """
        Plot that fills the area between two lines. If a single number is given for low, 
        extend it as a constant across the range of x.
        """
        # TODO : Small random string to differentiate names?
        # TODO : Could be some hash of input data, so that it does not change between runs
        self.add_plot_header("name path", "fill_between_lower")
        self.add_plot_header("sharp plot")
        self.buffer += self.generic_plot_headers(color=color)
        if len(low) < len(x):
            # Assume single value
            self.buffer += self.output_xy([x[0], x[-1]], [low[0], low[0]])
        else:
            # Full line
            self.buffer += self.output_xy(x, low)
        self.buffer += "};\n"
        # Reset name, plot the upper bound
        self.add_plot_header("name path", "fill_between_upper")
        self.buffer += self.generic_plot_headers(color=color)
        self.buffer += self.output_xy(x, high)
        self.buffer += "};\n"
        # Now, add the fill between plot
        fill_color = color
        if not fill_color:
            fill_color = "gray"
        self.buffer += "\\addplot[" + fill_color + "] fill between [of=fill_between_lower and fill_between_upper];\n"
        self.buffer += "\\addlegendentry{"+str(label)+"}\n"

    def colorline(self, x, y, c, linestyle="solid", cmap=False, label=False):
        # Header for colorbar -- TODO : Move to separate axes API
        self.add_header("colorbar")
        if cmap:
            self.add_header("colormap name", cmap)
        self.add_plot_header("point meta", "explicit")
        self.add_plot_header("mesh")
        self.add_plot_header("thick")
        #self.buffer += self.plotheader(linestyle=linestyle)
        self.buffer += self.generic_plot_headers()
        for i in range(len(x)):
            self.buffer += ("("+float_format+","+float_format+") ["+float_format+"]\n").format(x[i], y[i], c[i])
        self.buffer += self.plotfooter()
        if label:
            # TODO : Cannot separate the legend for single axis into several boxes
            # TODO : Also think about how to put legends from several axes into a single box
            # TODO : Different logo in the legend for the mesh setup
            self.buffer += "\\addlegendentry{"+str(label)+"}\n"

    def inset_axes(self, x, y, width, height):
        """
        Create the inset axes object
         - add coordinate reference to this axes
         - add at header to the new axes
        """
        new_axes = Axes()
        self.buffer += "\\coordinate (insetref"+str(self.inset_id)+") at (rel axis cs: "+str(x)+","+str(y)+");\n"
        new_axes.add_header("at", "{(insetref"+str(self.inset_id)+")}")
        if type(self.width) == float or type(self.width) == int:
            new_axes.width = self.width*width
        else:
            # String description assumed
            new_axes.width = str(width)+self.width
        if type(self.height) == float or type(self.height) == int:
            new_axes.height = self.height*height
        else:
            # String description assumed
            new_axes.height = str(height)+self.height
        self.inset_id += 1;
        return new_axes

    def twinx(self):
        """
        Create twin axes sharing the x axis
        """
        new_axes = Axes()
        if "at" in self.headers:
            new_axes.add_header("at", self.headers["at"])
        new_axes.width = self.width
        new_axes.height = self.height
        new_axes.add_header("axis x line", "none")
        new_axes.add_header("yticklabel pos", "right")
        new_axes.add_header("axis y line", "right")
        new_axes.add_header("y axis line style", "{-}")
        new_axes.add_header("ytick align", "inside")
        new_axes.xlim = self.xlim
        self.add_header("axis y line", "left")
        self.add_header("y axis line style", "{-}")
        self.add_header("ytick align", "inside")
        # TODO : does this count to inset id? Probably does not need to
        #self.inset_id += 1
        return new_axes

    def twiny(self):
        """
        Create twin axes sharing the y axis
        """
        new_axes = Axes()
        if "at" in self.headers:
            new_axes.add_header("at", self.headers["at"])
        new_axes.width = self.width
        new_axes.height = self.height
        new_axes.add_header("axis y line", "none")
        new_axes.add_header("xticklabel pos", "upper")
        new_axes.add_header("axis x line", "top")
        new_axes.add_header("x axis line style", "{-}")
        new_axes.add_header("xtick align", "inside")
        new_axes.ylim = self.ylim
        self.add_header("axis x line", "bottom")
        self.add_header("x axis line style", "{-}")
        self.add_header("xtick align", "inside")
        # TODO : does this count to inset id? Probably does not need to
        #self.inset_id += 1
        return new_axes

    def arrow(self, start, end, color="black", width=None, transform="data"):
        """
        Draws an arrow from start to end.
        - start, end: lists/tuples of (x, y)
        - relative: True for relative axes coordinates, False for data coordinates
        """
        coord_sys = transform_cs[transform]

        options = []
        if color:
            options.append(color)
        if width:
            # Using pt for line width in TikZ
            options.append(f"line width={width}pt")
        options.append(r"-{Latex}")
        if not ("arrows.meta" in self.extra_libs):
            self.extra_libs.append("arrows.meta")

        options_str = ",".join(options)

        cmd = ("\\draw[{}] ({}:"+float_format+","+float_format+") -- ({}:"+float_format+","+float_format+");").format(
            options_str, coord_sys, start[0], start[1], coord_sys, end[0], end[1]
        )

        self.add_patch(cmd)

    def rect_patch(self, pos_vec, rect_vec, relative=False):
        # Prepare the vertices
        vertices = [(pos_vec[0], pos_vec[1])]
        vertices.append((pos_vec[0] + rect_vec[0], pos_vec[1]))
        vertices.append((pos_vec[0] + rect_vec[0], pos_vec[1] + rect_vec[1]))
        vertices.append((pos_vec[0], pos_vec[1] + rect_vec[1]))
        vertices.append((pos_vec[0], pos_vec[1]))
        coord_sys = "axis cs"
        if relative:
            coord_sys = "rel axis cs"
        # Now, construct the command itself
        buffer = ("\\draw[solid] ("+coord_sys+":"+float_format+","+float_format+") --").format(vertices[0][0], vertices[0][1])
        for i in range(1,4):
            buffer += ("("+coord_sys+":"+float_format+","+float_format+") -- ").format(vertices[i][0], vertices[i][1])
        buffer += ("("+coord_sys+":"+float_format+","+float_format+");").format(vertices[4][0], vertices[4][1])
        return buffer

    def add_patch(self, patch):
        self.buffer += patch+"\n"

    def axline(self, coord, vert=False, color="black", style="solid"):
        # TODO : Axes coordinates?
        # Construct the style string
        styleString = "{"+",".join([style, color])+"}"
        if vert:
            self.extra_xtick_coords.append(coord)
            self.add_header("extra x tick style", "{grid=major,ticks=none,grid style="+styleString+"}")
            self.add_header("extra x tick labels", "{}")
        else:
            self.extra_ytick_coords.append(coord)
            self.add_header("extra y tick style", "{grid=major,ticks=none,grid style="+styleString+"}")
            self.add_header("extra y tick labels", "{}")

    def text(self, coord, text, transform="axes"):
        cs = transform_cs[transform]
        text_buffer = r"\node at ("+cs+":"+",".join(map(lambda x: float_format.format(x), coord))+")"
        text_buffer += " {"+text+"};\n"
        self.buffer += text_buffer
