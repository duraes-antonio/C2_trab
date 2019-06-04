from os import system as ossys
from platform import system as platsys


def instalar_dependencias():
	"""Tenta instalar a biblioteca matplotlib no sistema atual.

	Raises:
		ImportError: Se houver falha durante ou após instalar o matplotlib.
	"""

	# Tente importar matplotlib, se falhar, tente instalar
	try:
		from matplotlib import pyplot

	except ImportError:

		print("--> Instalando matplotlib, aguarde...")
		modulo = "matplotlib"
		codigo_instalacao = 0

		# Se for Windows, dê o comando, instale e limpe a tela
		if (platsys().upper() == "WINDOWS"):
			print("--> SO: WINDOWS")
			codigo_instalacao = ossys("pip install --user --quiet %s" %modulo)

		# Senão, é MAC ou Linux
		else:
			print("--> SO: LINUX")
			ossys("sudo apt install python3-tk python3-cycler 2>&1 >/dev/null")
			codigo_instalacao = ossys("pip3 install --user --quiet %s" %modulo)

		if codigo_instalacao != 0:
			raise ModuleNotFoundError("Não foi possível instalar o módulo '%s'" %modulo)