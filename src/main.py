from util import instalar_dependencias

instalar_dependencias()

from random import randint, uniform
from typing import List

from math import radians
from matplotlib import animation, pyplot
from matplotlib.patches import Wedge, Circle

from Ponto import PontoPolar


# Inicializa a estrutura do quadro onde os objetos serão desenhados
global_fig = pyplot.figure()
global_ax = global_fig.add_subplot(111, polar=True)

# Número de graus que o ângulo de abertura se incrementará no sentido anti-horário
global_increm_ang = 1

# Valor que a opacidade do setor variará a cada movimento
global_incremento_alpha = 0.01

# Fator que define se a opcidade incrementará ou decrementará
# Quando for 1, indica incremento; quando for -1, indica decremento
global_multip_alpha = 1

# Defina a largura e formato da linha da grade
global_ax.grid(linewidth=0.75)
global_pts_polar: List[PontoPolar] = []


def desenhar_triangulos() -> None:
	"""Marca no gráfico o 4 pontos triagulares nos extremos dos eixos e um central"""

	pyplot.polar(radians(0), 0, color="r", marker="^")
	pyplot.polar(radians(0), 2.9, color="r", marker=">")
	pyplot.polar(radians(90), 2.9, color="r", marker="^")
	pyplot.polar(radians(180), 2.9, color="r", marker="<")
	pyplot.polar(radians(270), 2.9, color="r", marker="v")


def desenhar_background(ax) -> None:
	"""Desenha o fundo da circunferência, projetando a sensação de gradiente"""

	decremento = 0.0104
	raio = 0.52
	cor = "#00{}0d"
	cor_atual = 20

	for i in range(40):
		circulo = Circle((0.5, 0.5), raio, transform=ax.transAxes)
		circulo.set_facecolor(cor.format(hex(cor_atual).split('x')[-1].zfill(2)))
		raio -= decremento
		cor_atual += 5
		ax.add_artist(circulo)


def sortear_pontos(quantidade: int, abert_min: float) -> List[PontoPolar]:
	"""Gera e retorna uma lista de pontos (contendo a tupla(theta, r))"""
	alpha_interv = abert_min + 360
	thetas = [randint(0, alpha_interv) for i in range(quantidade)]
	rs = [uniform(0.0, 2.6) for i in range(quantidade)]

	return [PontoPolar(theta, r) for theta, r in zip(thetas, rs)]


def plotar_pontos(min_theta, max_theta, pontos: List[PontoPolar]) -> None:
	# Para cada ponto na lista de entrada
	for pt in pontos:

		# Se o ponto tiver entre o theta mínimo e o máximo
		if max_theta >= pt.theta >= min_theta:

			if (pt.ponto_2d):
				pt.atualizar_alpha()

			else:
				temp_pt_2d, = pyplot.polar(radians(pt.theta), pt.r,
				                           color='#ff7e26', marker="o", alpha=0.1)
				pt.ponto_2d = temp_pt_2d

		else:
			if pt.ponto_2d:
				pt.ponto_2d.remove()
				pt.ponto_2d = None


def atualizar_setor(setor: Wedge, abertura_min: float) -> [Wedge]:
	"""Atualiza os valores de theta e opacidade do setor, movimentando-o"""

	global global_multip_alpha

	# O valor de theta = valor atual + incremento (Se a soma não ultrapassar 360)
	# Se a soma ultrapassar 360, o valor será o resto da divisão (soma / 360)
	setor.set_theta1((setor.theta1 + global_increm_ang) % 360)
	setor.set_theta2(setor.theta1 + abertura_min)

	# Se a opacidade do setor for maior que 0.4 ou for menor que o valor mínimo:
	# inverta de incremento para decremento ou vice-versa
	if setor.get_alpha() >= 0.4 or setor.get_alpha() < global_incremento_alpha:
		global_multip_alpha = (-1) * global_multip_alpha

	setor.set_alpha(setor.get_alpha() + global_incremento_alpha * global_multip_alpha)

	return [setor]


def atualizar_grafico(self, setor: Wedge, abertura_min: float):

	global global_pts_polar
	qtd_atual = len(global_pts_polar)
	global_pts_polar += sortear_pontos(7 - qtd_atual, abertura_min)

	atualizar_setor(setor, abertura_min)
	plotar_pontos(setor.theta1, setor.theta2, global_pts_polar)
	global_pts_polar = [pt for pt in global_pts_polar if pt.ponto_2d]


def main():
	desenhar_triangulos()
	desenhar_background(global_ax)
	abert_min = 45

	# Crie um setor de centro = (0.5, 0.5), r = 0.5, entre 0 e 45º
	# E adicione-o ao quadro
	setor: Wedge = Wedge((0.5, 0.5), 0.5, 0, abert_min, alpha=0.01, aa=True,
	                     color="white", transform=global_ax.transAxes)
	global_ax.add_artist(setor)

	# A cada K intervalo: movimente o setor e renderize a figura
	# com Q quadros por segundo
	temp = animation.FuncAnimation(global_fig, func=atualizar_grafico, frames=353,
	                               fargs=[setor, abert_min], interval=1)
	pyplot.show()

	return 0


main()
