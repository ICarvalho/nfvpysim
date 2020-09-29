from __future__ import division
import random
from nfvpysim.registry import register_vnf_placement
from collections import defaultdict


__all__ = [
    'random_policy',
          ]


def get_nfv_nodes(topology):
    return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']


def random_placement():
    dict_vnfs_cpu_req = {1: 15,  # nat
                         2: 25,  # fw
                         3: 25,  # ids
                         4: 20,  # wanopt
                         5: 20,  # lb
                         6: 25,  # encrypt
                         7: 25,  # decrypt
                         8: 30,  # dpi
                        }

    selected_vnfs = defaultdict()
    for vnf in range(1, random.randint(1,3)+1):
        target_vnf = random.choice(list(dict_vnfs_cpu_req.items()))
        if target_vnf not in selected_vnfs:
            for vnf, cpu in dict_vnfs_cpu_req.items():
                selected_vnfs[vnf] = cpu

    return selected_vnfs




def apply_vnfs_placement(placement, topology):
    for v, vnfs in placement.items():
        topology.node[v]['stack'][1]['n_vnfs'] = vnfs


##################################  VNF PLACEMENT POLICIES #############################################################

@register_vnf_placement('RANDOM')
def random_policy(topology, seed=None, **kwargs):
    random.seed(seed)
    nfv_nodes_candidates = get_nfv_nodes(topology)
    vnf_placement = defaultdict()
    vnfs = random_placement()
    for v in nfv_nodes_candidates:
        vnf_placement[v] = vnfs
    apply_vnfs_placement(vnf_placement, topology)





































