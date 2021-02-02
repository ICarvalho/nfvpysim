import networkx as nx
import random

def select_random_sfc():
    services = [
        [1, 2],  # [nat - fw]
        [4, 5],  # [wanopt - lb]
        [1, 2, 3],  # [nat - fw - ids]
        [2, 3, 5],  # [fw - ids - lb]
        [1, 5, 4],  # [nat - lb - wanopt]
        [5, 2, 1],  # [lb - fw - nat]
        [2, 3, 5, 6],  # [fw - ids - lb - encrypt]
        [3, 2, 5, 8],  # [ids - fw - lb - wanopt]
        [5, 4, 6, 2, 3],  # [lb - wanopt - encrypt - fw - ids]
    ]
    return random.choice(services)


def place_vnfs(G):
    for node in G.nodes():
        deg = nx.degree(G)
        nfv_nodes = [v for v in G if deg[v] == 2]
        if node in nfv_nodes:
            G.nodes[node]['name'] = 'nfv_node'
            G.nodes[node]['vnfs'] = select_random_sfc()
        else:
            G.nodes[node]['name'] = 'other_node'

    return G


G = nx.barbell_graph(10,10)
place_vnfs(G)

for node in G.nodes:
    if G.nodes[node]['name'] == 'nfv_node':
           for vnf in G.nodes[node]['vnfs']:
               print(node, G.nodes[node]['vnfs'][:])