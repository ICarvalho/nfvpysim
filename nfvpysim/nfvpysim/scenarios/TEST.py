import networkx as nx

G = nx.random_internet_as_graph(30)
a = [p for p in nx.all_shortest_paths(G, 0,11)]
print(a)