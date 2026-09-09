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
        for i in range(len(self.axes)):
            self.axes[i].save()
        self._figure.savefig(name)

class Axes(AxesBase):
    def __init__(self, figure):
        super().__init__(figure)
        self._axes = figure._figure.add_subplot(1,1,1)
        figure.axes.append(self)

    def save(self):
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
            self._axes.tick_params(axis="y", top=True, bottom=False, labeltop=True, labelbottom=False)
        if self.yticks_rotate != 0.0:
            self._axes.tick_params(axis="y", labelrotation=self.yticks_rotate, labelrotation_mode="ytick")
        # Axis labels
        if self.labels[0]:
            self._axes.set_xlabel(self.labels[0])
        if self.labels[1]:
            self._axes.set_ylabel(self.labels[1])
        # Legend
        if self.legend:
             self._axes.legend()

    def plot(self, x, y, label=False, color=False, linestyle=False):
        self._axes.plot(x, y, label=label, color=color, linestyle=linestyle)

    def scatter(self, x, y, label=False, color=False, markerstyle=False, linestyle="-"):
        self._axes.scatter(x, y,
                           label=label, c=color, marker=markerstyle, linestyle=linestyle)
