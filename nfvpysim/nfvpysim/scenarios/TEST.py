import itertools
from operator import itemgetter

import networkx as nx
from nfvpysim.scenarios.topology import *
from collections import OrderedDict
import fnss
from nfvpysim.execution.network import *
import random
from collections import defaultdict
from itertools import cycle



d = {'pw': 1, 'bw': 0.5}
a = sum(d.values())
print(a)









"""

l = [1, 2, 3, 4]
a = itertools.combinations(l,2)
#print(r)


def get_dist(topo, pairs):
    dist = {}
    for pair in pairs:
        dist[pair] = [nx.dijkstra_path(topo, pair[i], pair[i+1]) for n1 in range(len(pairs) for n2 in range(n1+1, len(pairs)))]
    return dist.values()
topo = topology_tatanld()
d = get_dist(topo, a)
print(d)
#print(d[(1, 2)])


"""



"""
from heapq import nlargest

# Initialize dictionary
test_dict = {'gfg' : 1, 'is' : 4, 'best' : 6, 'for' : 7, 'geeks' : 3 }

# Initialize N
N = 3

# printing original dictionary
print("The original dictionary is : " + str(test_dict))

# N largest values in dictionary
# Using nlargest
res = nlargest(N, test_dict, key = test_dict.get)

# printing result
print("The top N value pairs are  " + str(res))
"""






topo = topology_tatanld()
paths = dict(nx.all_pairs_shortest_path(topo))
node = 7
betw = nx.betweenness_centrality(topo)
#print(paths[20][30])
#print(betw)
#if node in topo.nodes:
    ##print(round(betw[node], 4))







"""
def calculate_all_shortest_paths(topology, ingress_node, egress_node):
    return [p for p in nx.all_shortest_paths(topology, ingress_node, egress_node)]
a = calculate_all_shortest_paths(topo, 1, 2)
print(a)

b = [[1, 3, 4], [2, 4, 4], [3, 4, 5]]

for l in a:
    for number in l:
        print(number)
"""



"""
la = [[1,2,3],10], [[2,3,5], 1000], [[1,0,0],2]
a = sorted(la, key=itemgetter(0))
print(a[0][0])
"""




"""
topo = topology_tatanld()
b = nx.betweenness_centrality(topo)
ord = dict(sorted(b.items(), key=lambda x: x[1], reverse=True))
print(b)
print()
print(ord)
print(dict(ord))
"""


"""
def select_random_sfc():
    services = {

        1: {'sfc': [1, 2, 3], 'delay': 120},
        2: {'sfc': [1, 5, 4], 'delay': 100},
        3: {'sfc': [2, 3, 5, 6], 'delay': 200},
        4: {'sfc': [3, 2, 5, 8], 'delay': 200},
        5: {'sfc': [3, 5, 6, 7], 'delay': 250},
        6: {'sfc': [3, 5, 2, 3, 4], 'delay': 300},
        7: {'sfc': [5, 4, 6, 2, 3], 'delay': 300},
        8: {'sfc': [3, 5, 6, 7, 8], 'delay': 320},

    }
    key = random.choice(list(services.keys()))
    return services[key]['sfc'], services[key]['delay']





def get_delay(service):
    services = {

        1: {'sfc': [1, 2, 3], 'delay': 120},
        2: {'sfc': [1, 5, 4], 'delay': 100},
        3: {'sfc': [2, 3, 5, 6], 'delay': 200},
        4: {'sfc': [3, 2, 5, 8], 'delay': 200},
        5: {'sfc': [3, 5, 6, 7], 'delay': 250},
        6: {'sfc': [3, 5, 2, 3, 4], 'delay': 300},
        7: {'sfc': [5, 4, 6, 2, 3], 'delay': 300},
        8: {'sfc': [3, 5, 6, 7, 8], 'delay': 320},

    }


def get_delay(dict_services, service):
    for k, v in dict_services.items():
        for k1, v1 in v.items():
            if v1 == service:
                return v.get('delay', v)



services = {

    1: {'sfc': [1, 2, 3], 'delay': 120},
    2: {'sfc': [1, 5, 4], 'delay': 100},
    3: {'sfc': [2, 3, 5, 6], 'delay': 200},
    4: {'sfc': [3, 2, 5, 8], 'delay': 200},
    5: {'sfc': [3, 5, 6, 7], 'delay': 250},
    6: {'sfc': [3, 5, 2, 3, 4], 'delay': 300},
    7: {'sfc': [5, 4, 6, 2, 3], 'delay': 300},
    8: {'sfc': [3, 5, 6, 7, 8], 'delay': 320},

}

a = get_delay(services, [1,2,3])
#print(a)


"""






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

sfcs = {
    1: [1, 2, 3],
    2: [1, 5, 4],
    3: [2, 3, 5, 6],
    4: [3, 2, 5, 8],
    5: [3, 5, 6, 7],
    6: [3, 5, 2, 3, 4],
    7: [5, 4, 6, 2, 3],
    8: [3, 5, 6, 7, 8],

}
    
    
    
    
"""


