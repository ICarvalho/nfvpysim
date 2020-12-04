from __future__ import division

from nfvpysim.registry import register_vnf_allocation

__all__ = [
    'static_vnf_allocation',
          ]



def get_nfv_nodes(topology):
    return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']



@register_vnf_allocation('STATIC')
def static_vnf_allocation(topology, cache_budget, **kwargs):

    nfv_nodes = get_nfv_nodes(topology)
    cache_size = cache_budget / 1
    for v in nfv_nodes:
        topology.node[v]['stack'][1]['n_vnfs'] = cache_size



