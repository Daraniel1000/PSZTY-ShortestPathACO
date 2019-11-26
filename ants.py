import networkx as nx
import parameters as par
import numpy as np
import readfile as rf
import time

graph = nx.Graph(shortest=float('inf'))
all_time_shortest_path = []
ants = []
alpha = par.ALPHA


class Ant:
	ant_id = 0

	def __init__(self, init_node, term_node):
		self.init_node = init_node
		self.term_node = term_node
		self.location = init_node
		self.vi_nodes = []
		self.path_length = 0
		self.is_returning = 0
		self.retsize = 1

		self.ant_id = Ant.ant_id
		Ant.ant_id += 1

	def pick_move(self):
		global alpha
		vi_ctr = 0
		possible_nodes = [n for n in graph[self.location]] # wczytaj sasiadow

		for n in possible_nodes: # zlicz sasiadow odwiedzonych
			if n in self.vi_nodes:
				vi_ctr += 1

		if vi_ctr < len(possible_nodes): # jesli nie wszyscy odwiedzeni, usun odwiedzonych
			for n in self.vi_nodes:
				if n in possible_nodes:
					possible_nodes.remove(n)

		row = np.array([graph[self.location][node]['pheromone'] for node in possible_nodes])
		dist = np.array([graph[self.location][node]['distance'] for node in possible_nodes])

		row = row ** alpha * ((1.0 / dist) ** par.BETA)  # liczymy tablicę prawdopodobieństw
		if row.sum() == 0:
			print("row.sum() = 0. mrówka:", self.ant_id, "wierzcholek:", self.location,
				  possible_nodes, row, self.vi_nodes)
			row += 1
		row = row / row.sum()
		# print("ant:", self.ant_id, "node:", self.location, "choices:", possible_nodes, "probs:", row)
		return np.random.choice(possible_nodes, 1, p=row)[0]  # i wybieramy nr wierzchołka następnego

	def step(self):
		next_node = self.init_node

		if self.is_returning == 1:
			next_node = self.vi_nodes.pop()
			new_pheromone = graph[next_node][self.location]['pheromone'] + self.retsize / self.path_length*graph[next_node][self.location]['distance']
			graph[next_node][self.location]['pheromone'] = min(par.MAX_PHER, new_pheromone)
		else:
			next_node = self.pick_move()
			self.vi_nodes.append(self.location)
			self.path_length += graph[self.location][next_node]['distance']

		self.location = next_node

		if self.location == self.term_node:
			self.is_returning = 1
			self.retsize = par.PHER_CONSTANT
			if self.path_length <= graph.graph['shortest']:
				self.retsize *= par.BIAS
				if self.path_length < graph.graph['shortest']:
					graph.graph['shortest'] = self.path_length
					global all_time_shortest_path
					all_time_shortest_path = np.copy(self.vi_nodes)
			# print("ant", self.ant_id, "path: ", self.path, self.path_length)
		elif self.location == self.init_node:
			self.path_length = 0
			self.vi_nodes.clear()
			self.is_returning = 0


def adjust_alpha(start): # niestabilna - zwiększenie alphy zaburza wynik
	global alpha
	edge_min = np.inf
	edge_max = 0
	for e in graph.edges(start):
		if graph[e[0]][e[1]]['distance'] > edge_max:
			edge_max = graph[e[0]][e[1]]['distance']
		if graph[e[0]][e[1]]['distance'] < edge_min:
			edge_min = graph[e[0]][e[1]]['distance']
	alpha *= min(20, edge_max / edge_min)


def aco_init():
	graph.update(rf.getgraph())

	#adjust_alpha(rf.start)
	#print(alpha)

	for k in range(par.NUM_OF_ANTS):
		ants.append(Ant(rf.start, rf.end))
	start = time.time()
	for i in range(par.STEPS):
		for a in ants:
			a.step()
		for u, v, p in graph.edges.data('pheromone'):
			graph[u][v]['pheromone'] = max(par.MIN_PHER, p*par.DECAY)
		print("time elapsed:", f"{time.time() - start:.15f}", end='\r')
	end = time.time()
	print("time elapsed:", f"{end - start:.15f}", "s")

aco_init()
print (graph.graph['shortest'], all_time_shortest_path)