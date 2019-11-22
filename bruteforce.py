import networkx as nx

graph = nx.Graph()
visited = []
tovisit = []


def bfs(node: int, dist: int):
    print(node)
    tovisit.pop(0)
    if graph.nodes[node]['dist'] == 0:
        graph.nodes[node]['dist'] = dist
    else:
        graph.nodes[node]['dist'] = min(graph.nodes[node]['dist'], dist)
    if visited[node] == 0:
        visited[node] = 1
        for nbr in graph[node]:
            if visited[nbr] == 0:
                tovisit.append((nbr, node))
    if len(tovisit) > 0:
        bfs(tovisit[0][0], graph.nodes[tovisit[0][1]]['dist'] + graph[tovisit[0][0]][tovisit[0][1]]['distance'])


fp = open("in.txt", "r")
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

tovisit.append((0, 0))
print(graph.edges)
bfs(start, 0)
print(graph.nodes[end]['dist'])
