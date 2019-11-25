import networkx as nx
import readfile as rf

graph = nx.Graph()
visited = []
tovisit = []


def bfs(node: int):
    tovisit.append((node, node))
    prev_node: int
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


graph.update(rf.getgraph())
for n in range(graph.size()):
    visited.append(0)
    graph.add_node(n, dist=0)

# tovisit.append((0, 0))
print(graph.edges)
bfs(rf.start)
print(graph.nodes[rf.end]['dist'])
