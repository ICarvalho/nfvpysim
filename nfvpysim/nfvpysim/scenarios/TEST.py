import networkx as nx
from nfvpysim.scenarios.topology import *
import fnss
from nfvpysim.execution.network import *
import random
from collections import defaultdict
from itertools import cycle


def var_len_seq_sfc():
    var_len_sfc = []
    sfcs = {1: 15,  # nat
            2: 25,  # fw
            3: 25,  # ids
            4: 20,  # wanopt
            5: 20,  # lb
            6: 25,  # encrypt
            7: 25,  # decrypts
            8: 30,  # dpi
            }
    sfc_len = random.randint(1, 8)
    sum_cpu = 0
    while sfc_len != 0:
        vnf, cpu = random.choice(list(sfcs.items()))
        if vnf not in var_len_sfc:
            var_len_sfc.append(vnf)
            sfc_len -= 1
            sum_cpu += cpu
            if sum_cpu > 100 or sfc_len == 0:
                break
            elif sum_cpu <= 100 and sfc_len != 0:
                sfc_len -= 1
    return var_len_sfc


def gen_var_len_sfc_to_nfv_nodes(n_sfcs):
    sfcs = []
    for i in range(1, n_sfcs + 1):
        sfc = var_len_seq_sfc()
        sfcs.append(sfc)
    return sfcs

a = gen_var_len_sfc_to_nfv_nodes(30)
print(a)

def vnfs_assignment(nfv_nodes, vnfs):
    if len(nfv_nodes) < len(vnfs):
        return dict(zip(cycle(nfv_nodes), vnfs))
    else:
        return dict(zip(nfv_nodes, cycle(vnfs)))







"""
opo = topology_kdl()
topo_nodes = topo.nodes 
ingress_nodes = random.sample(topo_nodes, 23)   # 23 nodes
egress_nodes = random.sample(topo_nodes, 23) # 23 nodes
nfv_nodes = random.sample(topo_nodes, 23)
"""


#path = nx.shortest_path(topo, 257, 22)
#nodes = list(topo.nodes)
#for node in path:
    #if topo.node[node]['stack'][0] == 'nfv_node':
        #print(node)
#print(sorted(ingress_nodes))
#print(sorted(egress_nodes))
#print(sorted(nfv_nodes))
"""
257 382 644 ing_nodes
512 22 40  egr_nodes
"""


"""
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


