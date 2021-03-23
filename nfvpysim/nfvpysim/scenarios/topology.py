from __future__ import division
import networkx as nx
import fnss
from nfvpysim.registry import register_topology_factory
import random


__all__ = [
        'NfvTopology',
        'topology_geant',
        'topology_tatanld',
        'topology_kdl',
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
        :return: return a set of ingress nodes
        """
        return set (v for v in self
                if 'stack' in self.node[v]
                and self.node[v]['stack'][0] == 'nfv_node'
                and 'cache_size' in self.node[v]['stack'][1])


    """
        def nfv_cache_nodes(self):
    
        return {v: self.node[v]['stack'][1]['cache_size']
                for v in self
                if 'stack' in self.node[v]
                and 'cache_size' in self.node[v]['stack'][1]
                }
    
    """


@register_topology_factory('GEANT')
def topology_geant(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Geant2012.graphml').to_undirected() # 61 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 8 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 2] # 13 nodes
    nfv_nodes = [v for v in topology.nodes() if deg[v] > 2 and v not in ingress_nodes + egress_nodes] #  19 nodes
    #forwarding_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes]
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)
    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})



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
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 9 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 2]  # 34 nodes
    nfv_nodes = [v for v in topology.nodes() if deg[v] > 2 ]   # 80 nodes
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # ttln
    # deg[v] == 1 = 9
    # deg[v] == 2 = 80
    # deg[v] == 3 = 34
    # deg[v] == 4 = 12
    # deg[v] == 5 = 7
    # deg[v] == 6 = 3



    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


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



@register_topology_factory('KDL')
def topology_kdl(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Kdl.graphml').to_undirected() # 754 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 42 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] > 2]  # 45 nodes
    nfv_nodes = [v for v in topology.nodes() if deg[v] == 2 and v not in ingress_nodes + egress_nodes]   # 483 nodes
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # kdl
    # deg[v] == 1 = 42
    # deg[v] == 2 = 483
    # deg[v] == 3 = 164
    # deg[v] == 4 = 45
    # deg[v] == 5 = 12
    # deg[v] == 6 = 6
    # deg[v] == 7 = 2


    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


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


@register_topology_factory('ION')
def topology_ion(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Garr200112.graphml').to_undirected() # 146  nodes
    topo_nodes = topology.nodes
    ingress_nodes = random.sample(topo_nodes, 5)   # 23 nodes
    #ingress_nodes = random.sample(topo_nodes, 23)   # 23 nodes
    egress_nodes = random.sample(topo_nodes, 5) # 23 nodes
    nfv_nodes = random.sample(topo_nodes, 10) # 50 nodes)
    topology.graph['nfv_nodes_candidates'] = nfv_nodes

    # ion
    # deg[v] == 1 = 11
    # deg[v] == 2 = 73
    # deg[v] == 3 = 33
    # deg[v] == 4 = 5
    # deg[v] == 5 = 2
    # deg[v] == 6 = 1


    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


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


@register_topology_factory('BESTEL')
def topology_bestel(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/RedBestel.graphml').to_undirected() # 84 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 10 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 4]  # 14 nodes
    nfv_nodes = [v for v in topology.nodes() if deg[v] == 2 and v not in ingress_nodes + egress_nodes]  # 54 nodes
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # bestel
    # deg[v] == 1 = 10
    # deg[v] == 2 = 54
    # deg[v] == 3 = 14
    # deg[v] == 4 = 5


    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


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
    topology = fnss.two_tier_topology(n_core=20, n_edge=40, n_hosts=20)

    # define ingress, egress and nfv nodes
    ingress_nodes = [v for v in random.sample(topology.hosts(), 20)]
    egress_nodes = [v for v in random.sample(topology.hosts(), 40) if v not in ingress_nodes]
    nfv_nodes = [v for v in random.sample(topology.hosts(), 400) if v not in ingress_nodes + egress_nodes ]
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # add stack on nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})



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

"""
topo = topology_bestel()
deg = nx.degree(topo)
node = [v for v in topo.nodes() if deg[v] == 5]
#print(nx.info(topo))
print(len(node))

"""

