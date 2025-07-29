from AxesPgfplots import AxesPgfplots as Axes, FigurePgfplots as Figure

f = Figure()
f.start()
a = Axes()
a.start()
a.plot([1,2,3,4], [1,4,9,16])
a.plot([1,2,3,4], [0,1,2,3])
a.end()
f.end()
