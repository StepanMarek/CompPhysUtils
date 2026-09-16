from compphysutils.graphics import Figure as FigureBase, Axes as AxesBase
import matplotlib

annotate_cs = {
    "data" : "data",
    "axes" : "axes fraction"
}

class Figure(FigureBase):
    def __init__(self):
        super().__init__()
        self.allowed_formats.append("png")
        self.allowed_formats.append("pdf")
        self.allowed_formats.append("svg")
        self._figure = matplotlib.figure.Figure()

    def save(self, name):
        # Figure width is governed by width in the first axes
        # DEBUG : Decide on figure vs. axes width
        # Inches conversion
        self._figure.set_figwidth(self.width / 2.54)
        self._figure.set_figheight(self.height / 2.54)
        #if len(self.axes) > 0:
        #    if self.axes[0].width:
        #        # Value passed must be in inches, stored value in cm
        #        self._figure.set_figwidth(self.axes[0].width / 2.54)
        #    if self.axes[0].height:
        #        # Value passed must be in inches, stored value in cm
        #        self._figure.set_figheight(self.axes[0].height / 2.54)
        for i in range(len(self.axes)):
            self.axes[i].save()
        self._figure.savefig(name)

class Axes(AxesBase):

    def __init__(self, figure=False, axes_obj=False):
        super().__init__(figure)
        if not axes_obj:
            if not figure:
                raise ValueError("Need to pass axis object or figure to Axes with matplotlib backend")
            else:
                self._axes = figure._figure.add_subplot(1,1,1)
        else:
            self._axes = axes_obj
        # Cumulative for labels -- to disable legend warnings
        self.legend_labels = False
        if figure:
            figure.axes.append(self)

    def save(self):
        """
        Sets the various axes options
        """
        # Axis limits
        if self.xlim:
            if self.xlim[0] or type(self.xlim[0]) != bool:
                self._axes.set_xlim(left=self.xlim[0])
            if self.xlim[1] or type(self.xlim[1]) != bool:
                self._axes.set_xlim(right=self.xlim[1])
        if self.ylim:
            if self.ylim[0] or type(self.ylim[0]) != bool:
                self._axes.set_ylim(bottom=self.ylim[0])
            if self.ylim[1] or type(self.ylim[1]) != bool:
                self._axes.set_ylim(top=self.ylim[1])
        # Ticks
        # xticks
        if self.xticks:
            if self.xtick_labels:
                self._axes.set_xticks(self.xticks, self.xtick_labels)
            else:
                self._axes.set_xticks(self.xticks)
        if self.xticks_swap:
            self._axes.tick_params(axis="x", top=True, bottom=False, labeltop=True, labelbottom=False)
        if self.xticks_rotate != 0.0:
            self._axes.tick_params(axis="x", labelrotation=self.xticks_rotate, labelrotation_mode="xtick")
        # yticks
        if self.yticks:
            if self.ytick_labels:
                self._axes.set_yticks(self.yticks, self.ytick_labels)
            else:
                self._axes.set_yticks(self.yticks)
        if self.yticks_swap:
            self._axes.tick_params(axis="y", left=False, right=True, labelleft=False, labelright=True)
        if self.yticks_rotate != 0.0:
            self._axes.tick_params(axis="y", labelrotation=self.yticks_rotate, labelrotation_mode="ytick")
        # width and height set in figure
        # Hiding axes
        if self.hide_axes == "both":
            self._axes.set_axis_off()
        elif self.hide_axes == "x":
            self._axes.xaxis.set_axis_off()
        elif self.hide_axes == "y":
            self._axes.yaxis.set_axis_off()
        # axis scaling handled in separate functions
        # axes line width
        if self.axes_linewidth:
            for spine in ["top", "bottom", "left", "right"]:
                self._axes.spines[spine].set_linewidth(self.axes_linewidth)
        # Axis labels
        if self.labels[0]:
            self._axes.set_xlabel(self.labels[0])
        if self.labels[1]:
            self._axes.set_ylabel(self.labels[1])
        # Legend
        legend_kwargs = {}
        if self.legend_pos:
            # translate
            pos_args = self.legend_pos.split()
            if len(pos_args) == 1:
                # just forward loc
                legend_kwargs["loc"] = pos_args[0]
            elif  len(pos_args) == 2:
                # just forward loc
                legend_kwargs["loc"] = " ".join(pos_args)
            elif len(pos_args) == 3:
                # Two coords, one loc
                legend_kwargs["loc"] = pos_args[0]
                legend_kwargs["bbox_to_anchor"] = (float(pos_args[1]), float(pos_args[2]))
            else:
                # Full spec
                legend_kwargs["loc"] = " ".join(pos_args[0:2])
                legend_kwargs["bbox_to_anchor"] = (float(pos_args[2]), float(pos_args[3]))
        if self.legend_cols:
            legend_kwargs["ncols"] = int(self.legend_cols)
        if self.legend and self.legend_labels:
            self._axes.legend(**legend_kwargs)

    def set_xscale(self, scale, base=10):
        self._axes.set_xscale(scale, base=base)

    def set_yscale(self, scale, base=10):
        self._axes.set_yscale(scale, base=base)

    def plot(self, x, y, label=False, color=False, linestyle=False):
        self._axes.plot(x, y, label=label, color=color, linestyle=linestyle)
        self.legend_labels = self.legend_labels or bool(label)

    def scatter(self, x, y, label=False, color=False, markerstyle=False, markersize=1.0, linestyle="-"):
        self._axes.scatter(x, y,
                           label=label, c=color, marker=markerstyle, s=markersize, linestyle=linestyle)
        self.legend_labels = self.legend_labels or bool(label)

    def errorbar(self, x, y, xerr=False, xmerr=False, yerr=False, ymerr=False, label=False, color=False, markerstyle=False, linestyle=False,
                 elinewidth=2, capsize=4, linewidth=0):
        # TODO : Asymmetric errorbars
        linestyle = linestyle if linestyle else None
        markerstyle = markerstyle if markerstyle else None
        color = color if color else None
        label = label if label else None
        self._axes.errorbar(x, y, xerr, yerr, color=color, linestyle=linestyle, marker=markerstyle, label=label,
                            elinewidth=elinewidth, capsize=capsize, linewidth=linewidth)
        self.legend_labels = self.legend_labels or bool(label)

    def colormap(self, x, y, c, label=None, cmap=None, norm=None, vmin=None, vmax=None):
        # Use pcolormesh, probably better than imshow, in principle also allows for quadriliterals instead of rectangles
        norm_translator = {
            "lin" : "linear"
        }
        self._axes.pcolormesh(x, y, c, label=label, cmap=cmap, shading="gouraud", norm=norm_translator[norm], vmin=vmin, vmax=vmax)
        self.legend_labels = self.legend_labels or bool(label)

    def colorline(self, x, y, c, linestyle="solid", cmap=None, label=None):
        # Construct a line collection
        segments = []
        colors = []
        for i in range(len(x)-1):
            segments.append([])
            segments[-1].append([x[i],y[i]])
            segments[-1].append([x[i+1],y[i+1]])
            # Interpolate the color
            colors.append(0.5 * (c[i] + c[i+1]))
        self._axes.add_collection(matplotlib.collections.LineCollection(segments, array=colors))
        # TODO : Labels

    def level(self, xs, lineoffset=0, linelength=1.0, orientation="vertical", label=None, color=None, linestyle=None):
        eplot = self._axes.eventplot(xs, orientation=orientation, linelengths=linelength, lineoffsets=lineoffset, label=label, color=color, linestyles=linestyle)
        self.legend_labels = self.legend_labels or bool(label)

    def quiver(self, x, y, u, v, label=None, color=None):
        # Call the quiver function
        # TODO : uv vs xy angles?
        self._axes.quiver(x, y, u, v, label=label, color=color, angles="xy", scale_units="xy", scale=1)
        self.legend_labels = self.legend_labels or bool(label)

    def fill_between(self, x, low, high, color=None, label=None):
        self._axes.fill_between(x, high, low, color=color, label=label)
        self.legend_labels = self.legend_labels or bool(label)

    def inset_axes(self, x, y, width, height):
        new_axes_obj = self._axes.inset_axes([x,y,width,height])
        new_axes = Axes(axes_obj=new_axes_obj)
        return new_axes

    def twinx(self):
        new_axes_obj = self._axes.twinx()
        new_axes = Axes(axes_obj=new_axes_obj)
        return new_axes

    def twiny(self):
        new_axes_obj = self._axes.twiny()
        new_axes = Axes(axes_obj=new_axes_obj)
        return new_axes

    def arrow(self, start=(0.0,0.0), end=(0.0,0.0), transform="data", linestyle="solid", width=1, color="black"):
        self._axes.annotate("", xy=end, xytext=start, xycoords=annotate_cs[transform], textcoords=annotate_cs[transform],
                            arrowprops={"width" : width, "color" : color, "linestyle" : linestyle})

    def axline(self, coord, vert=False, color="black", style="solid"):
        if vert:
            self._axes.axvline(coord, color=color, linestyle=style)
        else:
            self._axes.axhline(coord, color=color, linestyle=style)

    def text(self, coord, text, transform="axes"):
        self._axes.annotate(text, xy=coord, xycoords=annotate_cs[transform])

    def rect_patch(self, pos_vec, rect_vec, relative=False):
        transform=self._axes.transData
        if relative:
            transform=self._axes.transAxes
        rect = matplotlib.patches.Rectangle(xy=pos_vec, width=rect_vec[0], height=rect_vec[1], transform=transform,
                                            edgecolor="black", fill=False)
        return rect

    def add_patch(self, patch):
        self._axes.add_patch(patch)
