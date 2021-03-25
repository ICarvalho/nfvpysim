import networkx as nx
from nfvpysim.scenarios.topology import *
import fnss
from nfvpysim.execution.network import *
import random
from collections import defaultdict


for i in range(1, 10):
    a = random.uniform(10, 20)
    print(round(a,3))
    print("{:.2f}".format(a))




"""
topo = topology_kdl()
topo_nodes = topo.nodes
ingress_nodes = random.sample(topo_nodes, 23)   # 23 nodes
egress_nodes = random.sample(topo_nodes, 23)  # 23 nodes
nfv_nodes = random.sample(topo_nodes, 50)

#path = nx.shortest_path(topo, 257, 22)
#nodes = list(topo.nodes)
#for node in path:
    #if topo.node[node]['stack'][0] == 'nfv_node':
        #print(node)
print(sorted(ingress_nodes))
print(sorted(egress_nodes))
print(sorted(nfv_nodes))
"""





"""

257 382 644 ing_nodes
512 22 40  egr_nodes



path_dist = defaultdict(dict)
all_pairs_dist = dict(nx.all_pairs_shortest_path(topo))
ing_nodes = NetworkModelProposal.get_ingress_nodes(topo)
egr_nodes = NetworkModelProposal.get_egress_nodes(topo)

for ing_node in ing_nodes:
    for egr_node in egr_nodes:
        ing_egr_dist = all_pairs_dist[ing_node][egr_node]
        path_dist[ing_node][egr_node] = ing_egr_dist
        nfv_nodes = NetworkModelProposal.get_target_nfv_nodes_place_vnfs(topo)
        if any(v for v in ing_egr_dist):
            print("ingress node:", ing_node)
            print("egress node:", egr_node)
            print(path_dist[ing_node][egr_node])
            print(nfv_nodes)
"""


