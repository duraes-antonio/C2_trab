import matplotlib.pyplot as plt
import math
import numpy as np
import random

from matplotlib.lines import Line2D

qtd_pontos = 25

thetas = [math.radians(random.randint(0,360)) for i in range(qtd_pontos)]
rs = [random.uniform(0.0, 3.0) for i in range(qtd_pontos)]

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(projection="polar")

circle_thetas = np.arange(0, 360).astype("float64")
circle_thetas *= math.radians(1)
circle_r = [3] * 360

ax.fill(circle_thetas, circle_r, 'g')

line1, = plt.polar([0, math.radians(30)],[0, 3])
line2, = plt.polar([0, 0],[0, 3])

pts: [Line2D] = []
for x, y in zip(thetas, rs):
    line, = plt.polar(x, y, 'ro')
    pts.append(line)
    line.remove()

visible_pts = []

for theta in range(0, 360):
    max_degree = math.radians(30) + math.radians(theta)
    min_degree = math.radians(theta)

    line1.set_xdata(max_degree)
    line2.set_xdata(min_degree)

    for pt in pts:
        pt_theta = pt.get_xdata()
        if pt_theta >= min_degree and pt_theta <= max_degree and pt not in visible_pts:
            visible_pts.append(pt)
            ax.add_artist(pt)

        elif (pt_theta < min_degree or pt_theta > max_degree) and pt in visible_pts:
            visible_pts.remove(pt)
            pt.remove()

    plt.draw()
    plt.pause(0.01)

