import networkx as nx
import parameters as par
import random as ran
import numpy as np
import readfile as rf
import time

graph = nx.Graph(shortest=float('inf'))
all_time_shortest_path = []
ants = []
alpha_mul = 1


class Ant:
    ant_id = 0

    def __init__(self, init_node, term_node):
        self.init_node = init_node
        self.term_node = term_node
        self.location = init_node
        self.possible_nodes = []
        self.vi_nodes = []
        self.path = []
        self.path_length = 0
        self.is_returning = 0
        self.alpha = alpha_mul * par.ALPHA
        self.beta = par.BETA
        self.retsize = 1

        self.ant_id = Ant.ant_id
        Ant.ant_id += 1

    def pick_move(self):
        row = np.array([graph[self.location][node]['pheromone'] for node in self.possible_nodes])
        for n in self.vi_nodes:  # jeśli odwiedzone, to nie chcemy wracać
            if self.possible_nodes.count(n) > 0:
                row[self.possible_nodes.index(n)] = 0
        if row.sum() == 0:  # jeśli wszystkie odwiedzone
            row = np.array([graph[self.location][node]['pheromone'] for node in
                            self.possible_nodes])  # to nie bierzemy tego pod uwagę
        dist = np.array([graph[self.location][node]['distance'] for node in self.possible_nodes])
        row = row ** self.alpha * ((1.0 / dist) ** self.beta)  # liczymy tablicę prawdopodobieństw
        if row.sum() == 0:
            print("to się bardzo nie powinno zdaryć. mrówka:", self.ant_id, "wierzcholek:", self.location,
                  self.possible_nodes, row, self.path, self.vi_nodes)
            row += 1
        row = row / row.sum()
        nodes = np.copy(self.possible_nodes)
        # print("ant:", self.ant_id, "node:", self.location, "choices:", self.possible_nodes, "probs:", row)
        return np.random.choice(nodes, 1, p=row)[0]  # i wybieramy nr wierzchołka następnego

    def step(self):  #
        next_node = -1
        if self.is_returning == 1:
            next_node = self.vi_nodes.pop()
            new_pheromone = graph[next_node][self.location]['pheromone'] + self.retsize / self.path_length*graph[next_node][self.location]['distance']
            graph[next_node][self.location]['pheromone'] = min(par.MAX_PHER, new_pheromone)
        else:
            for nbr in graph[self.location]:
                self.possible_nodes.append(nbr)

            next_node = self.pick_move()
            self.vi_nodes.append(self.location)
            self.path_length += graph[self.location][next_node]['distance']

        self.location = next_node
        self.possible_nodes.clear()

        if self.location == self.term_node:
            self.is_returning = 1
            self.path = np.copy(self.vi_nodes)
            if self.path_length < graph.graph['shortest']:
                graph.graph['shortest'] = self.path_length
                self.retsize = par.BIAS * par.PHER_CONSTANT
                global all_time_shortest_path
                all_time_shortest_path = self.path
            else:
                if self.path_length == graph.graph['shortest']:
                    self.retsize = par.BIAS * par.PHER_CONSTANT
                else:
                    self.retsize = par.PHER_CONSTANT
            # print("ant", self.ant_id, "path: ", self.path, self.path_length)
        elif self.location == self.init_node:
            self.path_length = 0
            self.vi_nodes.clear()
            self.is_returning = 0


def adjust_alpha(start):
    global alpha_mul
    edge_min = np.inf
    edge_max = 0
    for e in graph.edges(start):
        if graph[e[0]][e[1]]['distance'] > edge_max:
            edge_max = graph[e[0]][e[1]]['distance']
        if graph[e[0]][e[1]]['distance'] < edge_min:
            edge_min = graph[e[0]][e[1]]['distance']
    #alpha_mul = min(20, edge_max ** 2 / edge_min)


def aco_init():
    graph.update(rf.getgraph())

    # adjust_alpha(rf.start)
    # print(alpha_mul)

    for k in range(par.NUM_OF_ANTS):
        ants.append(Ant(rf.start, rf.end))
    start = time.time()
    for i in range(par.STEPS):
        for a in ants:
            a.step()
        for u, v, p in graph.edges.data('pheromone'):
            p *= par.DECAY
            graph[u][v]['pheromone'] = max(par.MIN_PHER, p)
    end = time.time()
    print("time elapsed:", end-start, "s")
# for a in ants:
#	print(a.path, a.path_length)

# print("1 4", graph[1][4]['pheromone'], "\n1 2", graph[1][2]['pheromone'])


aco_init()
print (graph.graph['shortest'], all_time_shortest_path)