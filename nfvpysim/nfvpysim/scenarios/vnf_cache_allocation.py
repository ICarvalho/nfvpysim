from __future__ import division
from nfvpysim.registry import register_vnf_allocation
from nfvpysim.util import iround
import networkx as nx

__all__ = [
    'static_vnf_allocation',


          ]

@register_vnf_allocation('STATIC')
def static_vnf_allocation(topology, cache_budget, **kwargs):

    nfv_nodes_candidates = topology.graph['nfv_nodes_candidates']
    cache_size = cache_budget
    for v in nfv_nodes_candidates:
        topology.node[v]['stack'][1]['cache_size'] = cache_size
