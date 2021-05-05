import networkx as nx
from nfvpysim.scenarios.topology import *
import fnss
from nfvpysim.execution.network import *
import random
from collections import defaultdict
from itertools import cycle


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

a = select_random_sfc()[0]
print(a)




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
print(a)

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


    
    
    
    
"""


