from __future__ import division
import random
import networkx as nx

from tools.util import iround
from model.registry import register_vnf_allocation

__all__ = [
    'uniform_cache_placement',
          ]



def get_nfv_nodes(topology):
    return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']



@register_vnf_allocation('UNIFORM')
def uniform_cache_placement(topology, **kwargs):
    """Places cache budget uniformly across cache nodes.
    Parameters
    ----------
    topology : Topology
        The topology object

    """
    nfv_nodes = get_nfv_nodes(topology)
    cache_size = 7  # the maximum number of vnfs on the system
    for v in nfv_nodes:
        topology.node[v]['stack'][1]['n_vnfs'] = cache_size



