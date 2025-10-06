from compphysutils.graphics import AxesPgfplots as Axes, FigurePgfplots as Figure

f = Figure()
a = Axes()
a.plot([1,2,3,4], [1,4,9,16], color="red", linestyle="solid", markerstyle="square*", label="$x^2$")
a.errorbar([1,2,3,4], [0,1,2,3], yerr=[0.1, 0.2, 0.3, 0.4], color="green", label="$x-1$")
a.legend_cols = 2
a.legend_pos = "upper left"
f.axes.append(a)
f.save("test.pgf")
