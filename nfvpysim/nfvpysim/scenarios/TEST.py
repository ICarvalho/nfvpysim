import networkx as nx
from nfvpysim.scenarios.topology import topology_geant
from nfvpysim.execution.network import *
import random
from collections import defaultdict

topo = topology_geant()
path_dist = defaultdict(dict)
all_pairs_dist = dict(nx.all_pairs_shortest_path(topo))
ing_nodes = NetworkModelProposal.get_ingress_nodes(topo)
egr_nodes = NetworkModelProposal.get_egress_nodes(topo)
nfv_nodes = NetworkModelProposal.get_nfv_nodes(topo)

for ing_node in ing_nodes:
    for egr_node in egr_nodes:
        ing_egr_dist = all_pairs_dist[ing_node][egr_node]
        path_dist[ing_node][egr_node] = ing_egr_dist
        if any(v for v in ing_egr_dist):
            print("ingress node:", ing_node)
            print("egress node:", egr_node)
            print(path_dist[ing_node][egr_node])
