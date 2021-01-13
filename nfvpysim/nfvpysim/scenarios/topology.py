from __future__ import division
import networkx as nx
import fnss
from nfvpysim.registry import register_topology_factory
import random
import matplotlib.pyplot as plt

__all__ = [
        'NfvTopology',
        'topology_geant',
        'topology_tatanld',
        'topology_datacenter_two_tier'
        ]


INTERNAL_LINK_DELAY = 2
EXTERNAL_LINK_DELAY = 34



class NfvTopology(fnss.Topology):
    """ Class model for NFV-enable topology

    This topology is a simple FNSS topology with addition methods that return sets of nfv-nodes, routers/switches,
    ingress_nodes and egress_nodes.
    """



    def ingress_nodes(self):
        """
        :return: return a set of ingress nodes
        """
        return set (v for v in self
                if 'stack' in self.node[v]
                and self.node[v]['stack'][0] == 'ingress_node')



    def egress_nodes(self):
        """
        :return: return a set of egress nodes
        """

        return set (v for v in self
                    if 'stack' in self.node[v]
                    and self.node[v]['stack'][0] == 'egress_node')


    def nfv_nodes(self):
        """
        :return: return a set of egress nodes
        """

        return set (v for v in self
                    if 'stack' in self.node[v]
                    and self.node[v]['stack'][0] == 'nfv_node')





    @staticmethod
    def rand_var_len_seq_sfc():
        var_len_sfc = []
        sfcs = {1: 15,  # nat
                2: 25,  # fw
                3: 25,  # ids
                4: 20,  # wanopt
                5: 20,  # lb
                6: 25,  # encrypt
                7: 25,  # decrypts
                8: 30,  # dpi
                }
        sfc_len = random.randint(1, 8)
        sum_cpu = 0
        while sfc_len != 0:
            vnf, cpu = random.choice(list(sfcs.items()))
            if vnf not in var_len_sfc:
                var_len_sfc.append(vnf)
                var_len_sfc.append(cpu)
                sum_cpu += cpu
                sfc_len -= 1
                if sum_cpu > 100 or sfc_len == 0:
                    break
                elif sum_cpu <= 100 and sfc_len != 0:
                    sfc_len -= 1

        return var_len_sfc




@register_topology_factory('GEANT')
def topology_geant(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Geant2012.graphml').to_undirected() # 61 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 8 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 2] # 13 nodes
    nfv_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes] #  19 nodes


    vnfs_on_nfv_nodes = dict((v, []) for v in nfv_nodes)
    vnfs = NfvTopology.rand_var_len_seq_sfc()
    nfv_node = random.choice(nfv_nodes)
    for vnf in vnfs:
        vnfs_on_nfv_nodes[nfv_node].append(vnf)





    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'vnfs': vnfs_on_nfv_nodes[v]})



    # Set weight and delay on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    # label links as internal or external
    for u, v in topology.edges():
        if u in egress_nodes or v in egress_nodes:
            topology.adj[u][v]['type'] = 'external'
            # this prevents egress nodes to be used to route traffic
            fnss.set_weights_constant(topology, 1000.0, [(u, v)])
            fnss.set_delays_constant(topology, EXTERNAL_LINK_DELAY, 'ms', [(u, v)])
        else:
            topology.adj[u][v]['type'] = 'internal'

    return NfvTopology(topology)


@register_topology_factory('TATANLD')
def topology_tatanld(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/TataNld.graphml').to_undirected() # 186 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 80 nodes
    nfv_nodes = [v for v in topology.nodes() if deg[v] > 2]   # 34 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 2] # 22 nodes


    vnfs_on_nfv_nodes = dict((v, []) for v in nfv_nodes)
    vnfs = NfvTopology.rand_var_len_seq_sfc()
    nfv_node = random.choice(nfv_nodes)
    for vnf in vnfs:
        vnfs_on_nfv_nodes[nfv_node].append(vnf)

    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'vnfs': vnfs_on_nfv_nodes[v]})




    # Set weight and delay on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    # label links as internal or external
    for u, v in topology.edges():
        if u in egress_nodes or v in egress_nodes:
            topology.adj[u][v]['type'] = 'external'
            # this prevents egress nodes to be used to route traffic
            fnss.set_weights_constant(topology, 1000.0, [(u, v)])
            fnss.set_delays_constant(topology, EXTERNAL_LINK_DELAY, 'ms', [(u, v)])
        else:
            topology.adj[u][v]['type'] = 'internal'

    return NfvTopology(topology)


@register_topology_factory('DATACENTER_TWO_TIER')
def topology_datacenter_two_tier(**kwargs):
    # create a topology with 10 core switches, 20 edge switches and 10 hosts
    # per switch (i.e. 200 hosts in total)
    topology = fnss.two_tier_topology(n_core=10, n_edge=20, n_hosts=10)

    # define ingress, egress and nfv nodes
    ingress_nodes = [v for v in random.sample(topology.hosts(), 15)]
    egress_nodes = [v for v in random.sample(topology.hosts(), 15) if v not in ingress_nodes]
    nfv_nodes = [v for v in random.sample(topology.hosts(), 40) if v not in ingress_nodes + egress_nodes ]

    # add stack on nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    # assign capacities
    # let's set links connecting servers to edge switches to 1 Gbps
    # and links connecting core and edge switches to 10 Gbps.

    # get list of core_edge links and edge_leaf links
    link_types = nx.get_edge_attributes(topology, 'type')
    core_edge_links = [link for link in link_types if link_types[link] == 'core_edge']
    edge_leaf_links = [link for link in link_types if link_types[link] == 'edge_leaf']

    # assign capacities
    fnss.set_capacities_constant(topology, 1, 'Gbps', edge_leaf_links)
    fnss.set_capacities_constant(topology, 10, 'Gbps', core_edge_links)

    # assign weight 1 to all links
    fnss.set_weights_constant(topology, 1)

    # assign delay of 10 nanoseconds to each link
    fnss.set_delays_constant(topology, 10, 'ns')

    return NfvTopology(topology)



topo = topology_geant()
#nodes_deg = nx.degree(topo)
nx.draw(topo)
