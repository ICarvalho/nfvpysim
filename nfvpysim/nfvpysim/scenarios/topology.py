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
        'topology_datacenter_two_tier',
        'topology_bestel',
        'topology_ion',
        'topology_cogentco',
        'topology_interroute',
        'topology_colt',
        'topology_viatel',
        'topology_uscarrier',
        'topology_barabasi_albert',
        'topology_garr'

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


    def forwarding_nodes(self):
        """
        :return: return a set of egress nodes
        """

        return set (v for v in self
                    if 'stack' in self.node[v]
                    and self.node[v]['stack'][0] == 'forwarding_node')



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

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Geant2012.graphml').to_undirected() # 40 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 8 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 2] # 13 nodes
    nfv_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes]
    #forwarding_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes]
    topology.graph['nfv_nodes_candidates'] = nfv_nodes

    # GEANT
    # deg[v] == 1 = 8
    # deg[v] == 2 = 13
    # deg[v] == 3 = 5
    # deg[v] == 4 = 5
    # deg[v] == 5 = 6
    # deg[v] == 6 = 1

    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


    # Set weight and delay on all links
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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




@register_topology_factory('GARR')
def topology_garr(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Garr201201.graphml').to_undirected() # 40 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 8 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 2] # 13 nodes
    nfv_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes]
    #forwarding_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes]
    topology.graph['nfv_nodes_candidates'] = nfv_nodes

    # GEANT
    # deg[v] == 1 = 8
    # deg[v] == 2 = 13
    # deg[v] == 3 = 5
    # deg[v] == 4 = 5
    # deg[v] == 5 = 6
    # deg[v] == 6 = 1

    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


    # Set weight and delay on all links
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/TataNld.graphml').to_undirected() # 145 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 2]   # 9 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 3]  # 12 nodes
    nfv_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes]   # 124 nodes
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # TATANLD
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
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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
    egress_nodes = [v for v in topology.nodes() if deg[v] == 4]  # 45 nodes
    nfv_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes]   # 483 nodes
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
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Ion.graphml').to_undirected() # 125  nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 11 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 3] # 8 nodes
    nfv_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes] # 33 nodes
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
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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
    egress_nodes = [v for v in topology.nodes() if deg[v] == 3]  # 14 nodes
    nfv_nodes = [v for v in topology.nodes() if v not in ingress_nodes + egress_nodes]  # 54 nodes
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
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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



@register_topology_factory('USCARRIER')
def topology_uscarrier(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/UsCarrier.graphml').to_undirected() # 158 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 3]
    egress_nodes = [v for v in topology.nodes() if deg[v] == 4]
    nfv_nodes = [v for v in topology.nodes() if  v not in ingress_nodes + egress_nodes]
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # USCARRIER
    # deg[v] == 1 = 8
    # deg[v] == 2 = 101
    # deg[v] == 3 = 32
    # deg[v] == 4 = 14
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
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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


@register_topology_factory('VIATEL')
def topology_viatel(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/VtlWavenet2011.graphml').to_undirected() # 92 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]
    egress_nodes = [v for v in topology.nodes() if deg[v] == 4]
    nfv_nodes = [v for v in topology.nodes() if  v not in ingress_nodes + egress_nodes]
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # bestel
    # deg[v] == 1 = 1
    # deg[v] == 2 = 83
    # deg[v] == 3 = 7
    # deg[v] == 4 = 1


    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


    # Set weight and delay on all links
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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


@register_topology_factory('COGENTCO')
def topology_cogentco(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Cogentco.graphml').to_undirected() # 197 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]
    egress_nodes = [v for v in topology.nodes() if deg[v] == 4]
    nfv_nodes = [v for v in topology.nodes() if  v not in ingress_nodes + egress_nodes]
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # COGENTCO
    # deg[v] == 1 = 22
    # deg[v] == 2 = 95
    # deg[v] == 3 = 60
    # deg[v] == 4 = 13
    # deg[v] == 5 = 4
    # deg[v] == 6 = 4
    # deg[v] == 7 = 1
    # deg[v] == 8 = 0
    # deg[v] == 9 = 1
    # deg[v] == 10 = 0


    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


    # Set weight and delay on all links
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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


@register_topology_factory('COLT')
def topology_colt(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Colt.graphml').to_undirected() # 153 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 1]   # 10 nodes
    egress_nodes = [v for v in topology.nodes() if deg[v] == 2]  # 14 nodes
    nfv_nodes = [v for v in topology.nodes() if  v not in ingress_nodes + egress_nodes]  # 54 nodes
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # COLT
    # deg[v] == 1 = 55
    # deg[v] == 2 = 55
    # deg[v] == 3 = 25
    # deg[v] == 4 = 6
    # deg[v] == 5 = 5
    # deg[v] == 6 = 2
    # deg[v] == 7 = 1
    # deg[v] == 8 = 1
    # deg[v] == 9 = 1
    # deg[v] == 10 = 0


    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


    # Set weight and delay on all links
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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



@register_topology_factory('INTERROUTE')
def topology_interroute(**kwargs):

    topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Interoute.graphml').to_undirected() # 110 nodes
    deg = nx.degree(topology)
    ingress_nodes = [v for v in topology.nodes() if deg[v] == 3]   #
    egress_nodes = [v for v in topology.nodes() if deg[v] == 4]  #
    nfv_nodes = [v for v in topology.nodes() if  v not in ingress_nodes + egress_nodes]  #
    topology.graph['nfv_nodes_candidates'] = set(nfv_nodes)

    # INTERROUTE
    # deg[v] == 1 = 8
    # deg[v] == 2 = 53
    # deg[v] == 3 = 25
    # deg[v] == 4 = 19
    # deg[v] == 5 = 3
    # deg[v] == 6 = 2
    # deg[v] == 7 = 0
    # deg[v] == 8 = 0
    # deg[v] == 9 = 0
    # deg[v] == 10 = 0


    # Add stacks to nodes
    for v in ingress_nodes:
        fnss.add_stack(topology, v, 'ingress_node')

    for v in egress_nodes:
        fnss.add_stack(topology, v, 'egress_node')

    for v in nfv_nodes:
        fnss.add_stack(topology, v, 'nfv_node', {'cache_size': {}})


    # Set weight and delay on all links
    #fnss.set_weights_constant(topology, 1.0)
    #fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_geo_distance(topology, specific_delay=1, default_delay=1, delay_unit='ms')
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




@register_topology_factory('BARABASI_ALBERT')
def topology_barabasi_albert(**kwargs):
    # create a topology with 10 core switches, 20 edge switches and 10 hosts
    # per switch (i.e. 200 hosts in total)
    topology = fnss.glp_topology(350, 3, 5, 0.2, 0.48)


    ingress_nodes = random.sample(list(dict(topology.nodes)), 100)   # 100 random ingress nodes

    egress_nodes = random.sample(list(dict(topology.nodes)), 100)   # 100 random egress nodes

    nfv_nodes = [v for v in list(topology.nodes) if v not in ingress_nodes + egress_nodes]  #

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


#topo  = topology_colt()
#b = nx.betweenness_centrality(topo)
#print(b)

"""
topo = topology_barabasi_albert()
print("ingress_nodes:", topo.ingress_nodes())
print("egress_nodes:", topo.egress_nodes())
print("nfv_nodes:", topo.nfv_nodes())
print()
"""






"""
topo = topology_garr()

deg = nx.degree(topo)
node1 = [v for v in topo.nodes() if deg[v] == 1]
node2 = [v for v in topo.nodes() if deg[v] == 2]
node3 = [v for v in topo.nodes() if deg[v] == 3]
node4 = [v for v in topo.nodes() if deg[v] == 4]
node5 = [v for v in topo.nodes() if deg[v] == 5]
node6 = [v for v in topo.nodes() if deg[v] == 6]
node7 = [v for v in topo.nodes() if deg[v] == 7]
node8 = [v for v in topo.nodes() if deg[v] == 8]
node9 = [v for v in topo.nodes() if deg[v] == 9]
node10 = [v for v in topo.nodes() if deg[v] == 10]
#

print("Number of nodes of the topology:", topo.number_of_nodes())
print(" degree 1: ", len(node1), "nodes" " -->", node1)
print(" degree 2: ", len(node2), "nodes" " -->", node2)
print(" degree 3: ", len(node3), "nodes" " -->", node3)
print(" degree 4: ", len(node4), "nodes" " -->", node4)
print(" degree 5: ", len(node5), "nodes" " -->", node5)
print(" degree 6: ", len(node6), "nodes" " -->", node6)
print(" degree 7: ", len(node7), "nodes" " -->", node7)
print(" degree 8: ", len(node8), "nodes" " -->", node8)
print(" degree 9: ", len(node9), "nodes" " -->", node9)
print(" degree 10: ", len(node10), "nodes" " -->", node10)



"""






