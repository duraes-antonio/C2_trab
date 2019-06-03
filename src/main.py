import matplotlib.pyplot as plt
import math
import numpy as np
import random

from matplotlib.lines import Line2D
import matplotlib.colors as mcolors


def desenha_triangulos():
    plt.polar(math.radians(0), 2.9, color="r", marker=">")
    plt.polar(math.radians(90), 2.9, color="r", marker="^")
    plt.polar(math.radians(180), 2.9, color="r", marker="<")
    plt.polar(math.radians(270), 2.9, color="r", marker="v")


def desenha_background():
    # Circulo verde
    circle_thetas = np.arange(0, 360).astype("float64")
    circle_thetas *= math.radians(1)
    circle_r = [3] * 360
    ax.fill(circle_thetas, circle_r, 'g')

    fill_color = "#162e1a"
    zorder = 1

    # Gera gradiente
    z = np.empty((90, 1, 4), dtype=float)
    rgb = mcolors.colorConverter.to_rgb(fill_color)
    z[:, :, :3] = rgb
    z[:, :, -1] = np.linspace(1, 0, 90)[:, None]

    # Desenha gradientes no radar
    for quadrante in [0,1,2,3]:
        xmin, xmax, ymin, ymax = math.radians(quadrante*90), math.radians((quadrante * 90)+90), 0, 3
        im = ax.imshow(z, extent=[xmin, xmax, ymin, ymax], origin='upper', zorder=zorder)


def update_animation():
    """
    Exibe os pontos dentro do ângulo busca e deixa os pontos fora do angulo de busca invisiveis
    Faz as linhas andarem de acordo com o ângulo busca
    """

    # Faz o theta variar em 360 graus
    for theta in range(0, 360, 3):
        # Calcula o máximo e o mínimo grau do para o theta dentro do ângulo de busca
        max_degree = math.radians(angulo_busca) + math.radians(theta)
        min_degree = math.radians(theta)

        # Anda com as linhas 3 graus nos sentido anti-horário
        for i in range(angulo_busca + 1):
            degree = math.radians(i) + math.radians(theta)
            lines[i].set_xdata(degree)

        # Passa por todos os pontos
        for pt in pts:

            # Pega o theta do ponto
            pt_theta = pt.get_xdata()

            # Se o ponto tiver entre o theta mínimo e o máximo, e não estiver na lista de pontos visiveis
            if max_degree >= pt_theta >= min_degree and pt not in visible_pts:
                visible_pts.append(pt)  # Adiciona o ponto na lista de pontos visiveis
                ax.add_artist(pt)       # Deixa o ponto visivel no radar

            # Senão, e o ponto estiver fora do intervalo e ainda for visivel
            elif (pt_theta < min_degree or pt_theta > max_degree) and pt in visible_pts:
                visible_pts.remove(pt)  # Tira o ponto da lista de visiveis
                pt.remove()             # Deixa o ponto invisivel no radar

        plt.pause(0.01)


# Auto explicativo
qtd_pontos = 7
angulo_busca = 45

# Gera os pontos
thetas = np.array([math.radians(random.randint(0,360)) for i in range(qtd_pontos)])
rs = np.array([random.uniform(0.0, 3.0) for i in range(qtd_pontos)])

# Gera figura e adiciona um novo axes
fig = plt.figure()
ax = fig.add_subplot(projection="polar")

desenha_background()

min_alpha = 0.1
max_alpha = 0.6

# Gera lista de alphas para as linhas
# Entre o min_alpha e max_alpha
alphas = np.linspace(min_alpha, max_alpha, angulo_busca+1)

# Gera as linhas
lines = []
for i in range(angulo_busca + 1):
    lines.append(plt.polar([0, math.radians(i)],[0, 3], color="#002d04", alpha=alphas[i], linewidth=3)[0])

# Plota os pontos, e os deixa invisiveis
pts: [Line2D] = []
for theta, r in zip(thetas, rs):
    pt, = plt.polar(theta, r, color='#ff7e26', marker="o")  # Plota o ponto
    pts.append(pt)                                          # Add na lista
    pt.remove()                                             # Deixa o ponto invisivel

# Lista de pontos visiveis
visible_pts = []

# Loop Infinito
while True:
    update_animation()
