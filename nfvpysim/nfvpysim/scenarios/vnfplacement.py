from __future__ import division
import random
from nfvpysim.registry import register_vnf_placement
from collections import defaultdict
from nfvpysim.scenarios.topology import topology_geant


__all__ = [
    'random_placement'
          ]


def get_nfv_nodes(topology):
    return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']


def random_vnf_placement():
    dict_vnfs_cpu_req = {1: 15,  # nat
                         2: 25,  # fw
                         3: 25,  # ids
                         4: 20,  # wanopt
                         5: 20,  # lb
                         6: 25,  # encrypt
                         7: 25,  # decrypt
                         8: 30,  # dpi
                        }

    selected_vnfs = []
    sum_cpu = 0
    while sum_cpu < 100:
        target_vnf, cpu = random.choice(list((dict_vnfs_cpu_req.items())))
        if target_vnf not in selected_vnfs:
            selected_vnfs.append(target_vnf)
            sum_cpu += dict_vnfs_cpu_req[target_vnf]
            if sum_cpu > 100:
                break

    return selected_vnfs




def apply_vnfs_placement(placement, topology):
    for v, vnfs in placement.items():
        topology.node[v]['stack'][1]['n_vnfs'] = vnfs
        #print(v, vnfs)


##################################  VNF PLACEMENT POLICIES #############################################################

@register_vnf_placement('RANDOM')
def random_placement(topology, seed=None, **kwargs):
    random.seed(seed)
    nfv_nodes_candidates = get_nfv_nodes(topology)
    vnf_placement = defaultdict()
    for v in nfv_nodes_candidates:
        vnf_placement[v] = random_vnf_placement()
        #print(v, vnf_placement[v])
    apply_vnfs_placement(vnf_placement, topology)


"""
topo = topology_geant()
b = random_placement(topo)
print(b)

"""



















































