import argparse
from random import randint, uniform
from typing import List
from math import radians
from os import system as ossys
from platform import system as platsys
from util import instalar_dependencias

instalar_dependencias()

# Tente importar as bibliotecas mais especifícas
try:
	from matplotlib import animation, pyplot
	from matplotlib.patches import Wedge, Circle
	from Ponto import PontoPolar

except ModuleNotFoundError:

	# Se as bibliotecas estiverem instaladas, rechame o programa e limpe a tela
	if platsys().upper() == "WINDOWS":
		ossys("python main.py")

	else:
		ossys("python3 main.py")

	exit(0)

# Inicializa a estrutura do quadro onde os objetos serão desenhados
glob_fig = pyplot.figure()
glob_ax = glob_fig.add_subplot(111, polar=True)
glob_ax.grid(linewidth=0.75)

# Abertura do setor que realiza varredura
glob_abert_min = 45

# Número de graus que o ângulo de abertura se incrementará no sentido anti-horário
glob_increm_ang = 0.5

# Quantidade máxima de pontos gerados ao longo dos movimentos
glob_num_pontos = 7

# Valor que a opacidade do setor variará a cada movimento
glob_incremento_alpha = 0.01

# Fator que define se a opcidade incrementará ou decrementará
# Quando for 1, indica incremento; quando for -1, indica decremento
glob_multip_alpha = 1


def ler_argumentos():
	global glob_abert_min, glob_num_pontos, glob_increm_ang
	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--angulo", help="Angulo de abertura do setor que se movimenta",
	                    type=float, required=True)
	parser.add_argument("-p", "--pontos", help="Quantidade de pontos que serão plotados",
	                    type=int, required=True)
	parser.add_argument("-v", "--velocidade", help="Número de graus que o setor andará a cada movimento",
	                    type=float, required=True)
	argumentos = parser.parse_args()

	if argumentos.angulo: glob_abert_min = argumentos.angulo
	if argumentos.pontos: glob_num_pontos = argumentos.pontos
	if argumentos.pontos: glob_increm_ang = argumentos.velocidade


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
		cor_atual += 4
		ax.add_artist(circulo)


def sortear_pontos(quantidade: int, abert_min: float) -> List[PontoPolar]:
	"""Gera e retorna uma lista de pontos (contendo a tupla(theta, r))"""
	alpha_interv = 360
	thetas = [randint(0, alpha_interv) for i in range(quantidade)]
	rs = [uniform(0.0, 2.6) for i in range(quantidade)]

	return [PontoPolar(theta, r) for theta, r in zip(thetas, rs)]


def plotar_pontos(min_theta, max_theta, pontos: List[PontoPolar]) -> None:
	# Para cada ponto na lista de entrada
	for pt in pontos:

		theta = pt.theta + 360 if pt.theta < min_theta and pt.theta < max_theta else pt.theta

		# Se o ponto tiver entre o theta mínimo e o máximo
		if max_theta >= theta >= min_theta:

			if pt.ponto_2d:
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

	global glob_multip_alpha

	# O valor de theta = valor atual + incremento (Se a soma não ultrapassar 360)
	# Se a soma ultrapassar 360, o valor será o resto da divisão (soma / 360)
	setor.set_theta1((setor.theta1 + glob_increm_ang) % 360)
	setor.set_theta2(setor.theta1 + abertura_min)

	# Se a opacidade do setor for maior que 0.4 ou for menor que o valor mínimo:
	# inverta de incremento para decremento ou vice-versa
	if setor.get_alpha() >= 0.4 or setor.get_alpha() < glob_incremento_alpha:
		glob_multip_alpha = (-1) * glob_multip_alpha

	setor.set_alpha(setor.get_alpha() + glob_incremento_alpha * glob_multip_alpha)

	return [setor]


def atualizar_grafico(self, setor: Wedge, abertura_min: float, pontos: [PontoPolar]):
	atualizar_setor(setor, abertura_min)
	plotar_pontos(setor.theta1, setor.theta2, pontos)


def main():

	global glob_num_pontos, glob_abert_min

	ler_argumentos()
	desenhar_triangulos()
	desenhar_background(glob_ax)

	pts_polar: List[PontoPolar] = []
	pts_polar += sortear_pontos(glob_num_pontos, glob_abert_min)

	# Crie um setor de centro = (0.5, 0.5), r = 0.5, entre 0 e 45º
	# E adicione-o ao quadro
	setor: Wedge = Wedge((0.5, 0.5), 0.5, 0, glob_abert_min, alpha=0.01, aa=True,
	                     color="white", transform=glob_ax.transAxes)
	glob_ax.add_artist(setor)

	# A cada K intervalo: movimente o setor e renderize a figura
	# com Q quadros por segundo
	temp = animation.FuncAnimation(glob_fig, func=atualizar_grafico, frames=60,
	                               fargs=[setor, glob_abert_min, pts_polar], interval=3)
	pyplot.show()

	return 0


main()
