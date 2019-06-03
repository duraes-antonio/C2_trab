from matplotlib.lines import Line2D


class PontoPolar():

	def __init__(self, theta: float, r: float,
	             alpha_incr: float = 0.1):
		self.theta = theta
		self.r = r

		self.__ponto_2d = None
		self.__alpha_pt = 0
		self.__alpha_incremento = alpha_incr
		self.__fator_alpha = 1

	def atualizar_alpha(self):

		if(self.ponto_2d and (self.__alpha_pt > 0.99 or self.__alpha_pt < 0.1)):
			self.__fator_alpha = -1 * self.__fator_alpha

		if(self.ponto_2d):
			self.__alpha_pt += self.__alpha_incremento * self.__fator_alpha
			self.ponto_2d.set_alpha(self.__alpha_pt)

	@property
	def ponto_2d(self):
		return self.__ponto_2d

	@ponto_2d.setter
	def ponto_2d(self, ponto: Line2D):
		self.__ponto_2d = ponto

		if(ponto):
			temp_alpha = ponto.get_alpha()
			self.__alpha_pt = temp_alpha if temp_alpha else self.__alpha_incremento