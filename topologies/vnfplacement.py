
from model.nodes import VnfNode
from topologies.topology import topology_geant, topology_datacenter_two_tier, topology_tatanld
import random
from model.request import *
from model.nodes import *
from model.vnfs import *

@staticmethod
def add_vnf_on_node(vnf, node):

    return node.add_vnf(vnf)


def get_nfv_nodes_topo(topology):

    return topology.nfv_nodes()



def place_random_vnfs_on_nodes(vnfs, topology):

    nfv_nodes = get_nfv_nodes_topo(topology)
    for nfv_node in nfv_nodes:
        final_nodes = []
        if isinstance(nfv_node, VnfNode):
            for vnf in vnfs:
                add_vnf_on_node(vnf, nfv_node)
                final_nodes.append(nfv_node)
                print(nfv_node.get_vnfs())
    return final_nodes




topo = topology_geant()
nat = Nat()
fw = Firewall()
wan = WanOptimizer()
vnfs = [Nat(), Firewall(), Encrypter()]

nfv_nodes = topo.nfv_nodes()
placement = place_random_vnfs_on_nodes(vnfs, topo)
print(placement)
print(nfv_nodes)

