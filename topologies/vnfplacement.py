
from model.nodes import VnfNode
from topologies.topology import topology_geant, topology_datacenter_two_tier, topology_tatanld
import random
import fnss
from model.network import *
from model.request import *
from model.nodes import *
from model.vnfs import *

"""
def get_nfv_nodes( topology):
    if isinstance(topology, fnss.Topology):
        nfv_nodes = []
        for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'nfv_node':
                nfv_nodes.append(node)

        return nfv_nodes

"""




class VnfPlacement:

    def random_vnf_placement(self, topology, vnfs):

        if isinstance(topology, fnss.Topology):
            model = NetworkModel(topology)
            for nfv_node in nfv_nodes:
                if isinstance(nfv_node, VnfNode):
                    while nfv_node.get_sum_cpu_vnfs_on_vnf_node() <= nfv_node.get_rem_cpu():
                        random_vnf = random.choice(vnfs)
                        nfv_node.add_vnf_on_vnf_node(random_vnf)




"""


"""
topo = topology_geant()

nat = Nat()
lb = LoadBalancer()
fw = Firewall()
en = Encrypter()
de = Decrypter()
wan = WanOptimizer()

vnfs = [nat,  fw, lb, en, de, wan]

vnf_pl = VnfPlacement()

print(vnf_pl.random_vnf_placement(topo, vnfs))
print()
print(topo.nfv_nodes())
































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

