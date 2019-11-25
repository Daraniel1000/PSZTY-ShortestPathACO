import networkx as nx

graph = nx.Graph()
visited = []
tovisit = []


def bfs(node: int):
    tovisit.append((node, node))
    prev_node : int
    graph.add_edge(node, node, distance=0)
    while len(tovisit) > 0:
        prev_node = tovisit[0][0]
        node = tovisit[0][1]
        tovisit.pop(0)
        if graph.nodes[node]['dist'] == 0:
            graph.nodes[node]['dist'] = graph.nodes[prev_node]['dist'] + graph[prev_node][node]['distance']
        else:
            if graph.nodes[prev_node]['dist'] + graph[prev_node][node]['distance'] < graph.nodes[node]['dist']:
                graph.nodes[node]['dist'] = graph.nodes[prev_node]['dist'] + graph[prev_node][node]['distance']
            else:
                continue
        visited[node] = 1
        for nbr in graph[node]:
            if visited[nbr] == 0:
                tovisit.append((node, nbr))
            else:
                if graph.nodes[node]['dist'] + graph[node][nbr]['distance'] < graph.nodes[nbr]['dist']:
                    tovisit.append((node, nbr))

fp = open("out.txt", "r")
line = fp.readline()
num = list(line.split(" "))
start = int(num[0])
end = int(num[1])
graph.add_nodes_from(range(int(num[2])))

for line in fp:
    num = list(line.split(" "))
    graph.add_edge(int(num[0]), int(num[1]), distance=int(num[2]), pheromone=0)

for n in range(graph.size()):
    visited.append(0)
    graph.add_node(n, dist=0)

#tovisit.append((0, 0))
print(graph.edges)
bfs(start)
print(graph.nodes[end]['dist'])
