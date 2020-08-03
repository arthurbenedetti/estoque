import numpy
import random 

class Navio:

	destroyed = False
	placed = False
	place = []
	def __init__(self, tamanho, nome):
		self.tamanho = tamanho
		self.nome = nome
		

	def botar_Navio(self, tabuleiro, posX, posY, ori):
		if ori == 1 and self.placed == False and posX >= len(tabuleiro.mar) or posY + self.tamanho >= len(tabuleiro.mar) or posX < 0 or posY < 0:#limites do tabuleiro orientacao 1
			return "ship out of bounds"
		elif ori == 0 and self.placed == False and posX + self.tamanho >= len(tabuleiro.mar) or posX < 0 or posY < 0 or posY >= len(tabuleiro.mar):#limites do tabuleiro orientacao 2
			return "ship out of bounds"
		else:
			if ori == 1:
				for i in range(self.tamanho):
					tabuleiro.mar[posX][posY + i] = 1
					self.place.append(([posX],[posY + i]))
			else:
				for j in range(self.tamanho):
					tabuleiro.mar[posX + j][posY] = 1
					self.place.append(([posX + j],[posY]))
			self.placed = True

	def isDestroyed(self, jogo):
		cons = 0
		for i in range(self.tamanho):#passa parte por parte do Navio
			u = self.place[i]
			if jogo.mar[u[0][0]][u[1][0]] == 2: # compara se posicao no mar = 2 (hit)
				cons += 1
			else:
				cons = cons 
		if cons == self.tamanho:
			self.destroyed = True
			return self.destroyed
		else:
			self.destroyed = False
			return self.destroyed





class Jogo:
	mar = numpy.zeros((10, 10), dtype=int)#faz uma matriz de zeros

	def atirar(self, posX, posY):
		if posX >= len(self.mar) or posY >= len(self.mar):
			return "guess out of bounds"
		else:
			self.mar[posX][posY] = 2
			return "shot at" + str([posX])+ "and" + str([posY])



jogador = Jogo()
inimigo = Jogo()

Navios_jog = []
Navios_ini = []

portaAviao_jog = Navio(5,"uss gerald ford")
encoracado_jog1 = Navio(4, "uss strong monkey")
encoracado_jog2 = Navio(4, "uss strong fish")
fragata_jog1 = Navio(3, "uss mini monkey")
fragata_jog2 = Navio(3, "uss mini fish")
submarino_jog1 = Navio(2, "sub 1")
submarino_jog2 = Navio(2, "sub 2")
Navios_jog.append(portaAviao_jog)
Navios_jog.append(encoracado_jog1)
Navios_jog.append(encoracado_jog2)
Navios_jog.append(fragata_jog1)
Navios_jog.append(fragata_jog2)
Navios_jog.append(submarino_jog1)
Navios_jog.append(submarino_jog2)


portaAviao_ini = Navio(5,"china ping")
encoracado_ini1 = Navio(4, "china ling")
encoracado_ini2 = Navio(4, "china xing")
fragata_ini1 = Navio(3, "china ming")
fragata_ini2 = Navio(3, "china hing")
submarino_ini1 = Navio(2 , "sub china ming")
submarino_ini2 = Navio(2, "sub china ling")
Navios_ini.append(portaAviao_ini)
Navios_ini.append(encoracado_ini1)
Navios_ini.append(encoracado_ini2)
Navios_ini.append(fragata_ini1)
Navios_ini.append(fragata_ini2)
Navios_ini.append(submarino_ini1)
Navios_ini.append(submarino_ini2)

for Navio in Navios_jog:
	X = input("escolha posicao x do Navio")
	Y = input("escolha posicao y do Navio")
	ori = input("esolha orientacao 0 horizontal, 1 vertical")
	Navio.botar_Navio(jogador.mar, X, Y, ori)

for Navio in Navios_ini:
	Navio.botar_Navio(inimigo.mar, random.randint(0,10), random.randint(0,10), random.randint(1))

print(jogador.mar, end = " ")
print(inimigo.mar)