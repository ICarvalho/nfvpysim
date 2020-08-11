from __future__ import division
import random
from nfvpysim.model.registry import register_vnf_placement
from collections import defaultdict


__all__ = [
    'uniform_vnf_placement',
          ]


def get_nfv_nodes(topology):
    return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']


def select_target_vnfs():

    dict_vnfs_cpu_req = {1: 15,  # nat
                         2: 25,  # fw
                         3: 25,  # ids
                         4: 20,  # wanopt
                         5: 20,  # lb
                         6: 25,  # encrypt
                         7: 25   # decrypt
                        }

    sum_vnfs_cpu = 0
    selected_vnfs = set()
    while sum_vnfs_cpu <= 100:
        for vnf in range(1, 8):
            target_vnf = random.choice(list(dict_vnfs_cpu_req.keys()))
            if target_vnf not in selected_vnfs:
                selected_vnfs.add(target_vnf)
                sum_vnfs_cpu += dict_vnfs_cpu_req[target_vnf]
            if sum_vnfs_cpu >= 100:
                break

    return selected_vnfs



def apply_vnfs_placement(placement, topology):

    for v, vnfs in placement.items():
        topology.node[v]['stack'][1]['n_vnfs'] = vnfs



@register_vnf_placement('UNIFORM')
def uniform_vnf_placement(topology, seed=None, **kwargs):

    random.seed(seed)
    nfv_nodes_candidates = get_nfv_nodes(topology)
    vnf_placement = defaultdict(set)
    vnfs = select_target_vnfs()
    for v in nfv_nodes_candidates:
        topology.node[v]['stack'][1]['n_vnfs'] = vnfs
    apply_vnfs_placement(vnf_placement, topology)


