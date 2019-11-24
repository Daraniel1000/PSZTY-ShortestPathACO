import networkx as nx
import parameters as par
import random as ran
import numpy as np

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
        self.path = []
        # self.vi_edges = []
        self.path_length = 0
        self.is_returning = 0
        self.alpha = par.ALPHA
        self.beta = par.BETA

        self.vi_nodes.append(init_node)
        self.ant_id = Ant.ant_id
        Ant.ant_id += 1

    # def calculate_coef(self):
    #	for node in self.possible_nodes:
    #		graph[self.location][node]['coef'] = ran.random()

    def pick_move(self):
        row = np.array([graph[self.location][node]['pheromone'] for node in self.possible_nodes])
        for n in self.vi_nodes:                         # jeśli odwiedzone, to nie chcemy wracać
            if self.possible_nodes.count(n) > 0:
                row[self.possible_nodes.index(n)] = 0
        if row.sum() == 0:                              # jeśli wszystkie odwiedzone
            row = np.array([graph[self.location][node]['pheromone'] for node in self.possible_nodes])  # to nie bierzemy tego pod uwagę
        dist = np.array([graph[self.location][node]['distance'] for node in self.possible_nodes])
        row = row ** self.alpha * ((1.0 / dist) ** self.beta)       # liczymy tablicę prawdopodobieństw
        row = row / row.sum()
        nodes = np.copy(self.possible_nodes)
       # print("ant:", self.ant_id, "node:", self.location, "choices:", self.possible_nodes, "probs:", row)
        return np.random.choice(nodes, 1, p=row)[0]                 # i wybieramy nr wierzchołka następnego

    def step(self):  #
        next_node = -1
        best_coef = -1

        if self.is_returning == 1:
            next_node = self.vi_nodes.pop()
            graph[next_node][self.location]['pheromone'] += 1 / self.path_length
        else:
            for nbr in graph[self.location]:
                self.possible_nodes.append(nbr)

            # self.calculate_coef()

            # for node in self.possible_nodes:                            # TODO
            #	if graph[self.location][node]['coef'] > best_coef:
            #		best_coef = graph[self.location][node]['coef']
            #		next_node = node
            #	elif graph[self.location][node]['coef'] == best_coef and ran.random() > 0.5:
            #		next_node = node

            next_node = self.pick_move()
            # self.vi_edges.append((self.location, next_node))
            self.vi_nodes.append(self.location)
            self.path_length += graph[self.location][next_node]['distance']

        self.location = next_node
        self.possible_nodes.clear()

        if self.location == self.term_node:
            self.is_returning = 1
            self.path = np.copy(self.vi_nodes)
            print("ant ", self.ant_id, "path: ", self.path, self.path_length)
        elif self.location == self.init_node:
            self.path_length = 0
            self.vi_nodes.clear()
            self.is_returning = 0

    def test(self):
        self.step()
        # print('ant', self.ant_id, 'location: ' + str(self.location))
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
        graph.add_edge(int(num[0]), int(num[1]), distance=int(num[2]), pheromone=0.1, coef=0)

    for n in range(graph.size()):
        graph.add_node(n)

    for k in range(par.NUM_OF_ANTS):
        ants.append(Ant(start, end))

    for i in range(50):
        for a in ants:
            a.test()
        for u, v, p in graph.edges.data('pheromone'):
            p *= par.DECAY
            graph[u][v]['pheromone'] = p


aco_init()
