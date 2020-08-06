from __future__ import division
import random
import networkx as nx

from tools.util import iround
from model.registry import register_cache_placement


__all__ = [
    'uniform_cache_placement',
          ]


def get_nfv_nodes(topology):

    return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']


def select_target_vnfs():

    dict_vnfs_cpu_req = {'1': 15,  # nat
                         '2': 25,  # fw
                         '3': 30,  # ids
                         '4': 20,  # wanopt
                         '5': 30,  # lb
                         '6': 40,  # encrypt
                         '7': 40   # decrypt
                        }

    n_vnfs = random.randint(1, len(dict_vnfs_cpu_req) + 1)
    sum_vnfs_cpu = 0
    selected_vnfs = set()
    for vnf in range(1, n_vnfs + 1):
        while sum_vnfs_cpu <= 100:
            target_vnf = random.choice(dict_vnfs_cpu_req.keys())
            if target_vnf not in selected_vnfs:
                selected_vnfs.add(target_vnf)
                sum_vnfs_cpu += dict_vnfs_cpu_req[target_vnf]
                if sum_vnfs_cpu == 100:
                    break
    return selected_vnfs




@register_cache_placement('UNIFORM')
def uniform_cache_placement(topology, cache_budget, **kwargs):

    nfv_nodes_candidates = get_nfv_nodes(topology)
    cache_size = iround(cache_budget / len(nfv_nodes_candidates))
    for v in nfv_nodes_candidates:
        topology.node[v]['stack'][1]['cache_size'] = cache_size
