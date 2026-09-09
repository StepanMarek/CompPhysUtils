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
    def __init__(self, figure):
        super().__init__(figure)
        self._axes = figure._figure.add_subplot(1,1,1)
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
                self._axes.set_xlim(left=self.xlim[1])
        if self.ylim:
            if self.ylim[0] or type(self.ylim[0]) != bool:
                self._axes.set_ylim(left=self.ylim[0])
            if self.ylim[1] or type(self.ylim[1]) != bool:
                self._axes.set_ylim(left=self.ylim[1])
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
        if self.legend:
            self._axes.legend(**legend_kwargs)
        # TODO : Legend cols, legend pos

    def set_xscale(self, scale, base=10):
        self._axes.set_xscale(scale, base=base)

    def set_yscale(self, scale, base=10):
        self._axes.set_yscale(scale, base=base)

    def plot(self, x, y, label=False, color=False, linestyle=False):
        self._axes.plot(x, y, label=label, color=color, linestyle=linestyle)

    def scatter(self, x, y, label=False, color=False, markerstyle=False, markersize=1.0, linestyle="-"):
        self._axes.scatter(x, y,
                           label=label, c=color, marker=markerstyle, s=markersize, linestyle=linestyle)
