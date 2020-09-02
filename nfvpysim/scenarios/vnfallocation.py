from __future__ import division

from nfvpysim.registry import register_vnf_allocation

__all__ = [
    'uniform_cache_placement',
          ]



def get_nfv_nodes(topology):
    return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']



@register_vnf_allocation('UNIFORM')
def uniform_cache_placement(topology, **kwargs):

    nfv_nodes = get_nfv_nodes(topology)
    n_vnfs = 7  # the maximum number of vnfs on the system
    for v in nfv_nodes:
        topology.node[v]['stack'][1]['n_vnfs'] = n_vnfs



