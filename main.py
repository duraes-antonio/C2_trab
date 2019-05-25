import matplotlib.pyplot as plt
import math
import numpy as np
import random

from matplotlib.lines import Line2D

qtd_pontos = 25
angulo_busca = 45

min_alpha = 0.2
max_alpha = 0.6

thetas = np.array([math.radians(random.randint(0,360)) for i in range(qtd_pontos)])
rs = np.array([random.uniform(0.0, 3.0) for i in range(qtd_pontos)])

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(projection="polar")

circle_thetas = np.arange(0, 360).astype("float64")
circle_thetas *= math.radians(1)
circle_r = [3] * 360
ax.fill(circle_thetas, circle_r, 'g')

alphas = np.array([(max_alpha - min_alpha) * i / (angulo_busca + 1) + min_alpha for i in range(angulo_busca + 2)])

lines = []
for i in range(angulo_busca + 1):
    lines.append(plt.polar([0, math.radians(i)],[0, 3],color="#162e1a", alpha=alphas[i], linewidth=1)[0])

pts: [Line2D] = []
for x, y in zip(thetas, rs):
    line, = plt.polar(x, y, color='#00ff24',marker="o")
    pts.append(line)
    line.remove()

visible_pts = []

while True:
    for theta in range(0, 360):
        max_degree = math.radians(angulo_busca) + math.radians(theta)
        min_degree = math.radians(theta)

        for i in range(angulo_busca + 1):
            degree = math.radians(i) + math.radians(theta)
            lines[i].set_xdata(degree)

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
