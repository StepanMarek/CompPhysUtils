from compphysutils.graphics import AxesPgfplots as Axes, FigurePgfplots as Figure

f = Figure()
a = Axes()
a.plot([1,2,3,4], [1,4,9,16], color="red", linestyle="dashed")
a.plot([1,2,3,4], [0,1,2,3], color="green", linestyle="dotted")
f.axes.append(a)
f.save("test.pgf")
