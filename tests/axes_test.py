from compphysutils.graphics import AxesPgfplots as Axes, FigurePgfplots as Figure
from numpy import sin

# Data
n = 40
x = []
y = []
c = []
dx = 1.0/(n-1)
x0 = -0.5
dy = 1.0/(n-1)
y0 = -0.5
for i in range(n):
    x.append([])
    y.append([])
    c.append([])
    for j in range(n):
        x[i].append(i*dx + x0)
        y[i].append(j*dy + y0)
        c[i].append(sin(5*x[i][-1] + 5*y[i][-1]))

f = Figure()
a = Axes()
a.colormap(x,y,c)
a.xlim = [-0.5, 0.5]
a.ylim = [-0.5, 0.5]
f.axes.append(a)
f.save("cmap.pgf")
