from __future__ import division

from os import path
import networkx as nx
import fnss
import random
from model.nodes import VnfNode, IngressNode, EgressNode, ForwardingNode



INTERNAL_LINK_DELAY = 2
EXTERNAL_LINK_DELAY = 34


class NfvTopology(fnss.Topology):
    """ Class model for NFV-enable topology

    This topology is a simple FNSS topology with addition methods that return sets of nfv-nodes, routers/switches,
    ingress_nodes and egress_nodes.
    """

    def nfv_nodes(self):
        """
        :return: return a set of nfv nodes
        """

        return {v: self.node[v]['stack'][0]['id'][1]['cpu'][2]['ram'][3]['r_cpu'][4]['r_ram']
                for v in self
                if 'stack' in self.node[v]
                and 'id' in self.node[v]['stack'][0]
                and 'cpu' in self.node[v]['stack'][1]
                and 'ram' in self.node[v]['stack'][2]
                and 'r_cpu' in self.node[v]['stack'][3]
                and 'r_ram' in self.node[v]['stack'][4]
                }




    def ingress_nodes(self):
        """
        :return: return a set of ingress nodes
        """

        return {v: self.node[v]['stack'][1]['id'] for v in self
                if 'stack' in self.node[v]
                and self.node[v]['stack'][1] == 'ingress_node'
                }






    def egress_nodes(self):
        """
        :return: return a set of egress nodes
        """

        return {v: self.node[v]['stack'][1]['id'] for v in self
                if 'stack' in self.node[v]
                and self.node[v]['stack'][1] == 'egress_node'
                }



    def forwarding_nodes(self):
        """
        :return: return a set of forwarding nodes (generic nodes for general topology)
        """

        return {v: self.node[v]['stack'][1]['id'] for v in self
                if 'stack' in self.node[v]
                and self.node[v]['stack'][1] == 'fw_node'
                }


    def router_nodes(self):
        """
        :return: return a set of router nodes (for datacenter topology)
        """

        return set (v for v in self
                    if 'stack' in self.node[v]
                    and self.node[v]['stack'][0] == 'router_node')



    def switch_nodes(self):
        """
        :return: return a set of router nodes (for datacenter topology)
        """

        return set (v for v in self
                    if 'stack' in self.node[v]
                    and self.node[v]['stack'][0] == 'switch_node')




def topology_geant(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/datasets/Geant2012.graphml').to_undirected() # 61 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 8 nodes
    nfv_nodes = [v for v in topology.nodes() if deg[v] > 2]   # 19 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 2] # 13 nodes
    forwarding_nodes = [v for v in topology.nodes() if v not in ingress_nodes + nfv_nodes+ egress_nodes] # 14 nodes

    # Add stacks to nodes
    ing_node = IngressNode()
    for v in ingress_nodes:

        fnss.add_stack(topology, v, 'ingress_node', {'id': ing_node.get_node_id()})


    nfv_node = VnfNode()
    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'id': nfv_node.get_node_id(),
                                                'cpu': nfv_node.get_cpu(),
                                                'ram': nfv_node.get_ram(),
                                                'r_cpu': nfv_node.get_rem_cpu(),
                                                'r_ram': nfv_node.get_ram()})


    egr_node = EgressNode()
    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node', {'id': egr_node.get_node_id()})



    fw_node = ForwardingNode()
    for v in forwarding_nodes:
        fnss.add_stack(topology, v, 'forwarding_node', {'id': fw_node.get_node_id()})


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



def topology_tatanld(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/datasets/TataNld.graphml').to_undirected() # 186 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 80 nodes
    nfv_node = [v for v in topology.nodes() if deg[v] > 2]   # 34 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 2] # 22 nodes
    forwarding_nodes = [v for v in topology.nodes() if v not in ingress_nodes + nfv_node + egress_nodes] # 9 nodes

    # Add stacks to nodes
    ing_node = IngressNode()
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node', {'id': ing_node.get_node_id()})

    vnf_node = VnfNode()
    for v in nfv_node:
        fnss.add_stack(topology, v, 'nfv_node', {'id': vnf_node.get_node_id(),
                                                 'cpu': vnf_node.get_cpu(),
                                                 'ram': vnf_node.get_ram(),
                                                 'r_cpu': vnf_node.get_rem_cpu(),
                                                 'r_ram': vnf_node.get_rem_ram()})
    egr_node = EgressNode()
    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node', {'id': egr_node.get_node_id()})

    for v in forwarding_nodes:
        fw_node = ForwardingNode()
        fnss.add_stack(topology, v, 'forwarding_node', {'id': fw_node.get_node_id()})


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

def topology_datacenter_two_tier():
    # create a topology with 10 core switches, 20 edge switches and 10 hosts
    # per switch (i.e. 200 hosts in total)
    topology = fnss.two_tier_topology(n_core=10, n_edge=20, n_hosts=10)

    # define ingress, egress and nfv nodes
    ingress_nodes = [v for v in random.sample(topology.hosts(), 15)]
    egress_nodes = [v for v in random.sample(topology.hosts(), 15) if v not in ingress_nodes]
    nfv_nodes = [v for v in random.sample(topology.hosts(), 40) if v not in ingress_nodes + egress_nodes ]

    # add stack on nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v , 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v , 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v , 'nfv_node')



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
print(topo.nfv_nodes())
