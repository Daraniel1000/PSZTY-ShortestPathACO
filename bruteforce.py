import sys

import networkx as nx
import readfile as rf
import time

graph = nx.Graph()
visited = []
tovisit = []
path = []
path_len = int(sys.maxsize)


def dfs(node, end, len, visited: []):
    if type(visited) != list:
        print("type error")
        return
    visited.append(node)
    if node == end:
        global path_len, path
        if len < path_len:
            path_len = len
            path = visited.copy()
    else:
        for nbr in graph[node]:
            if visited.count(nbr) == 0:
                dfs(nbr, end, len + graph[node][nbr]['distance'], visited)
                # print(nbr, "out")
    visited.pop()


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
            graph.nodes[node]['parent'] = prev_node
        else:
            if graph.nodes[prev_node]['dist'] + graph[prev_node][node]['distance'] < graph.nodes[node]['dist']:
                graph.nodes[node]['dist'] = graph.nodes[prev_node]['dist'] + graph[prev_node][node]['distance']
                graph.nodes[node]['parent'] = prev_node
            else:
                continue
        visited[node] = 1
        for nbr in graph[node]:
            if visited[nbr] == 0:
                tovisit.append((node, nbr))
            else:
                if graph.nodes[node]['dist'] + graph[node][nbr]['distance'] < graph.nodes[nbr]['dist']:
                    tovisit.append((node, nbr))


def dfs_print(node):
    if node != rf.start:
        dfs_print(graph.nodes[node]['parent'])
    print(node, end=' ')


graph.update(rf.getgraph())
for n in range(graph.size()):
    visited.append(0)
    graph.add_node(n, dist=0, parent=0)

# tovisit.append((0, 0))
# print(graph.edges)
start = time.time()
dfs(rf.start, rf.end, 0, [])
print(path_len, path)
# print(graph.nodes[rf.end]['dist'], end=' ')
# dfs_print(rf.end)
# print()
end = time.time()
print("time elapsed:", end - start, "s")
