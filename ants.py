import networkx as nx
import parameters as par
import random as ran

graph = nx.Graph()
ants = []


class Ant:
	ant_id = 0

	def __init__(self, init_node, term_node):
		self.init_node = init_node
		self.term_node = term_node
		self.location = init_node
		self.possible_nodes = []
		self.vi_nodes = []
		self.vi_edges = []
		self.length_travelled = 0
		self.is_returning = 0

		self.vi_nodes.append(init_node)
		self.ant_id = Ant.ant_id
		Ant.ant_id += 1

	def calculate_coef(self):
		for node in self.possible_nodes:
			graph[self.location][node]['coef'] = ran.random()

	def step(self):
		next_node = -1
		best_coef = -1

		if self.is_returning == 1:
			next_node = self.vi_nodes.pop()
		else:		
			for nbr in graph[self.location]:
					self.possible_nodes.append(nbr)

			self.calculate_coef()

			for node in self.possible_nodes:
				if graph[self.location][node]['coef'] > best_coef:
					best_coef = graph[self.location][node]['coef']
					next_node = node
				elif graph[self.location][node]['coef'] == best_coef and ran.random() > 0.5:
					next_node = node
		self.location = next_node
		if self.is_returning == 0:
			self.vi_edges.append((self.location, next_node))
			self.vi_nodes.append(self.location)
			self.length_travelled += 1
		self.possible_nodes.clear()

		if self.location == self.term_node:
			self.is_returning = 1
			self.vi_nodes.pop()
		elif self.location == self.init_node:
			self.is_returning = 0

	def test(self):
		self.step()
		print('ant', self.ant_id, 'location: '+str(self.location))
		return


def aco_init():
	fp = open("in.txt", "r")
	line = fp.readline()
	num = list(line.split(" "))
	start = int(num[0])
	end = int(num[1])
	graph.add_nodes_from(range(int(num[2])))

	for line in fp:
		num = list(line.split(" "))
		graph.add_edge(int(num[0]), int(num[1]), distance=int(num[2]), pheromone=0, coef=0)

	for n in range(graph.size()):
		graph.add_node(n)

	for k in range(par.NUM_OF_ANTS):
		ants.append(Ant(start, end))

	for i in range(5):
		for a in ants:
			a.test()


aco_init()
