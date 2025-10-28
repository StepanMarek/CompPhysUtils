from compphysutils.graphics.plotter import backendModules
from numpy import sin

pgf = backendModules["pgfplots"]
pgf["spec"].loader.exec_module(pgf["module"])
f = pgf["module"].Figure()
a = pgf["module"].Axes()

# Data
n = 20
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

a.colormap(x,y,c)
a.xlim = [-0.5, 0.5]
a.ylim = [-0.5, 0.5]
a.xticks_rotate = 90
a.yticks_rotate = 45
f.axes.append(a)
f.width=4
f.height=3
f.save("cmap.pgf")
