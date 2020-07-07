import random
import collections

from fnss.util import random_from_pdf


def apply_vnf_placement(placement, topology):

    for v, vnfs in placement.items():
        topology.node[v]['stack'][1]['vnfs'] = vnfs

def get_vnf_location(topology):
    return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']


def uniform_content_placement(topology, vnfs, seed=None):

    random.seed(seed)
    vnf_nodes = get_vnf_location(topology)
    vnf_placement = collections.defaultdict(set)
    for c in vnfs:
        vnf_placement[random.choice(vnf_nodes)].add(c)
    apply_vnf_placement(vnf_placement, topology)