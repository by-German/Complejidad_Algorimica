import pygame
from collections import deque
# i:
from Wall import Wall

class Player:
	def __init__(self, fila, columna, n, color, nro_walls):
		self.x = fila
		self.y = columna
		self.n = n
		self.turn = False 
		self.origen = 0
		self.destino = 0
		self.color = color
		self.wall = []
		self.can_move = True
		# temp
		self.camino = []

	def event_key(self, event):

		pass
	
	def draw(self, screen, size):
		self.tam = size[0] / self.n
		# dibujo del jugador
		tam = int(200 / self.n )
		pygame.draw.circle(screen, self.color, (self.x, self.y), tam)

		# temp: dibujo del wall
		for wall in self.wall:
			wall.draw(screen, self.color, self.tam)
	
	def update(self):
		pass

	def next_movement(self, origen, destinos, G): # orgigen posicion jugador
		self.camino = []
		# lanza bfs
		self.BFS(G, G.nodes[origen])
		# halla camino
		self.camino = self.road_manager(G, origen, destinos)
		# self.hallar_camino(G, G.nodes[origen], G.nodes[destino], self.camino)
		if len(self.camino) == 0: return self.origen
		return self.camino[0]
		# if len(self.camino) == 1: # llego al destino
		# 	self.camino.append(destino)
		# 	return self.camino[0]# self.camino[0:2]
		# return self.camino[1] #camino[:2] # return 2 next positions

	def BFS(self, G, s):
		s["color"] = "gris"
		s["distancia"] = 0
		s["p"] = None
		Q = deque()
		Q.append(s)  # enqueue
		while not (Q == deque([])):
			u = Q.popleft()
			for _, v in G.edges(u["id"]):
				nodo = G.nodes[v]
				if nodo["color"] == "blanco":
					nodo["color"] = "gris"
					nodo["distancia"] = u["distancia"] + 1
					nodo["p"] = u # -> u = nodo
					Q.append(nodo)
			u["color"] = "negro"
		return

	def road_manager(self, G, origen, destinos) -> list:
		caminos = [[] for _ in range(len(destinos))]
		for id, destino in enumerate(destinos): self.hallar_camino(G, G.nodes[origen], G.nodes[destino], caminos[id])
		camino = caminos[0]
		for id, road in enumerate(caminos):
			if len(camino) > len(road): camino = road
		return camino

	def hallar_camino(self, G, s, v, camino):
		if v["id"] == s["id"]:
			# camino.append(s["id"]) # agrega el ultimo camino faltante
			pass
		elif v["p"] == None: 
			print("No existe camino de {} a {}".format(s["id"], v["id"]))
		else:
			self.hallar_camino(G, s, v["p"], camino)
			camino.append(v["id"]) # agrega todos los caminos 
		return

	def place_wall(self, G, origen, fin):
		xi, yi = G.nodes[origen]["pos"]
		xf, yf = G.nodes[fin]["pos"]
		if xi == xf: ## nodos vericales -> Muro horizontal
			y = abs(yf + yi) // 2 # la resta es para que encaje en la generacion
			self.wall.append(Wall(xi - (self.tam // 2), y, origen, fin, horizontal = True))
		elif yi == yf: ## hotizotal
			x = abs(xf + xi) // 2
			self.wall.append(Wall(x, yi - (self.tam // 2), origen, fin, horizontal = False))
		G.remove_edge(origen, fin) # se remueve el muro -- > se quita la arista en el grafo

	def remove_wall(self, G):
		# self.wall.pop()
		# G.add_edge(self.wall.orgien, self.wall.fin)
		# self.wall.
	 	# podemos retornar la posicion para poner el wall o sino aqui mismo ponerlo
		pass