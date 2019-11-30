import networkx as nx

start: int
end: int

def getgraph():
    graph = nx.Graph()
    fp = open("out.txt", "r")
    line = fp.readline()
    num = list(line.split(" "))
    global start
    start = int(num[0])
    global end
    end = int(num[1])
    graph.add_nodes_from(range(int(num[2])))
    for line in fp:
        num = list(line.split(" "))
        graph.add_edge(int(num[0]), int(num[1]), distance=int(num[2]), pheromone=1.0)
    return graph
