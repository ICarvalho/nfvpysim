import networkx as nx
import fnss
from itertools import cycle
import random
from collections import defaultdict
from nfvpysim.registry import CACHE_POLICY
from nfvpysim.util import path_links
from collections import OrderedDict
from operator import itemgetter
import logging

# from multi_key_dict import multi_key_dict
logger = logging.getLogger('orchestration')

__all__ = [
    'NetworkModelFirstOrder',
    'NetworkModelBaseLine',
    'NetworkModelProposal',
    'NetworkViewFirstOrder',
    'NetworkViewBaseLine',
    'NetworkViewProposal',
    'NetworkController'
]

class NetworkViewTapAlgo:

    def __init__(self, model):
        if not isinstance(model, NetworkModelBaseLine):
            raise ValueError('The model argument must be an instance of '
                             'NetworkModel')

        self.model = model

    def shortest_path(self, ingress_node, egress_node):
        return self.model.shortest_path[ingress_node][egress_node]

    def all_pairs_shortest_paths(self):
        return self.model.shortest_path

    def nfv_cache_nodes(self, size=True):
        return {v: c.maxlen for v, c in self.model.nfv_cache.items()} if size \
            else list(self.model.nfv_cache.keys())

    def is_nfv_node(self, node):
        return node in self.model.nfv_cache

    def link_type(self, u, v):
        return self.model.link_type[(u, v)]

    def link_delay(self, u, v):
        return self.model.link_delay[(u, v)]

    def topology(self):
        return self.model.topology



class NetworkViewBaseLine:

    def __init__(self, model):
        if not isinstance(model, NetworkModelBaseLine):
            raise ValueError('The model argument must be an instance of '
                             'NetworkModel')

        self.model = model

    def shortest_path(self, ingress_node, egress_node):
        return self.model.shortest_path[ingress_node][egress_node]

    def all_pairs_shortest_paths(self):
        return self.model.shortest_path

    def nfv_cache_nodes(self, size=True):
        return {v: c.maxlen for v, c in self.model.nfv_cache.items()} if size \
            else list(self.model.nfv_cache.keys())

    def is_nfv_node(self, node):
        return node in self.model.nfv_cache

    def link_type(self, u, v):
        return self.model.link_type[(u, v)]

    def link_delay(self, u, v):
        return self.model.link_delay[(u, v)]

    def topology(self):
        return self.model.topology


class NetworkViewFirstOrder:

    def __init__(self, model):
        if not isinstance(model, NetworkModelFirstOrder):
            raise ValueError('The model argument must be an instance of '
                             'NetworkModel')

        self.model = model

    def shortest_path(self, ingress_node, egress_node):
        return self.model.shortest_path[ingress_node][egress_node]

    def all_pairs_shortest_paths(self):
        return self.model.shortest_path

    def nfv_cache_nodes(self, size=True):
        return {v: c.maxlen for v, c in self.model.nfv_cache.items()} if size \
            else list(self.model.nfv_cache.keys())

    def is_nfv_node(self, node):
        return node in self.model.nfv_cache

    def link_type(self, u, v):
        return self.model.link_type[(u, v)]

    def link_delay(self, u, v):
        return self.model.link_delay[(u, v)]

    def topology(self):
        return self.model.topology


class NetworkViewProposal:

    def __init__(self, model):
        if not isinstance(model, NetworkModelProposal):
            raise ValueError('The model argument must be an instance of '
                             'NetworkModel')

        self.model = model

    def shortest_path(self, ingress_node, egress_node):
        return self.model.shortest_path[ingress_node][egress_node]

    def all_pairs_shortest_paths(self):
        return self.model.shortest_path

    def nfv_cache_nodes(self, size=True):
        return {v: c.maxlen for v, c in self.model.nfv_cache.items()} if size \
            else list(self.model.nfv_cache.keys())

    def is_nfv_node(self, node):
        return node in self.model.nfv_cache

    def link_type(self, u, v):
        return self.model.link_type[(u, v)]

    def link_delay(self, u, v):
        return self.model.link_delay[(u, v)]

    def topology(self):
        return self.model.topology


class NetworkModelTapAlgo:
    """
    Models the internal state of the network.
    This object should never be edited by VNF Allocation Policies directly, but only
    through calls to the network controller.

    """

    def __init__(self, topology, nfv_cache_policy, shortest_path=None):  #

        if not isinstance(topology, fnss.Topology):
            raise ValueError('The topology argument must be an'
                             'instance of fnss.Topology or   of its subclasses')

        self.shortest_path = dict(shortest_path) if shortest_path is not None \
            else (dict(nx.all_pairs_dijkstra_path(topology)))

        self.topology = topology
        self.nfv_cache = None

        self.link_type = nx.get_edge_attributes(topology, 'type')
        self.link_delay = fnss.get_delays(topology)

        if not topology.is_directed():
            for (u, v), link_type in list(self.link_type.items()):
                self.link_type[(v, u)] = link_type

            for (u, v), delay in list(self.link_delay.items()):
                self.link_delay[(v, u)] = delay

        nfv_cache_size = {}
        for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'nfv_node':
                if 'cache_size' in stack_props:
                    nfv_cache_size[node] = stack_props['cache_size']
        if any(c < 8 for c in nfv_cache_size.values()):
            logger.warning('Some nfv node caches have size less than 8.'
                           'I am setting them to 8 and run the experiment anyway')
            for node in nfv_cache_size:
                if nfv_cache_size[node] < 8:
                    nfv_cache_size[node] = 8

        # use when the len(vnfs) < len(nfv_nodes)
        def vnfs_assignment(nfv_nodes, vnfs):
            if len(nfv_nodes) < len(vnfs):
                return dict(zip(cycle(nfv_nodes), vnfs))
            else:
                return dict(zip(nfv_nodes, cycle(vnfs)))

        policy_name = nfv_cache_policy['name']
        # policy_name = 'NFV_CACHE'
        policy_args = {k: v for k, v in nfv_cache_policy.items() if k != 'name'}
        # The actual cache objects storing the vnfs
        self.nfv_cache = {node: CACHE_POLICY[policy_name](nfv_cache_size[node], **policy_args)
                          for node in nfv_cache_size}

        # for node in self.nfv_cache:
        # print(node)
        # self.nfv_cache[node].list_nfv_cache()
        # sfcs = [[5, 7, 8, 3], [7, 6], [5, 4, 2], [2, 5, 3, 7], [1, 3] ]


        # place a single vnf in all nfv-nodes
        """
        target_nfv_nodes = vnfs_assignment(self.nfv_cache, sfcs)
        for node in self.nfv_cache:
            if node in target_nfv_nodes.keys():
                # print(node)
                vnf = target_nfv_nodes[node]
                # for vnf in sfc:
                self.nfv_cache[node].add_vnf(vnf)
                # self.nfv_cache[node].list_nfv_cache()
        """


        """
        target_nfv_nodes = vnfs_assignment(self.nfv_cache, sfcs)
        for node in self.nfv_cache:
            if node in target_nfv_nodes.keys():
                #print(node)
                vnfs = target_nfv_nodes[node]
                for vnf in vnfs:
                    self.nfv_cache[node].add_vnf(vnf)
                    #self.nfv_cache[node].list_nfv_cache()
        
        """


    @staticmethod
    def shortest_path(topology, ingress_node, egress_node):
        return nx.shortest_path(topology, ingress_node, egress_node)

    @staticmethod
    def calculate_all_shortest_paths(topology, ingress_node, egress_node):
        return [p for p in nx.all_shortest_paths(topology, ingress_node, egress_node)]

    @staticmethod
    def get_ingress_nodes(topology):

        if isinstance(topology, fnss.Topology):
            ing_nodes = []
            for node in topology.nodes():
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'ingress_node':
                    ing_nodes.append(node)

            return ing_nodes

    @staticmethod
    def get_egress_nodes(topology):

        if isinstance(topology, fnss.Topology):
            egr_nodes = []
            for node in topology.nodes():
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'egress_node':
                    egr_nodes.append(node)

            return egr_nodes

    @staticmethod
    def get_nfv_nodes(topology):
        return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']

    def get_nfv_nodes_path(self, path):

        nfv_nodes = []
        for node in path:
            if self.topology.node[node]['stack'][0] == 'nfv_node':
                nfv_nodes.append(node)
        return nfv_nodes

    def get_ingress_node_path(self, path):
        for node in path:
            return self.topology.node[node]['stack'][0] == 'ingress_node'

    def get_egress_node_path(self, path):
        for node in path:
            return self.topology.node[node]['stack'][0] == 'egress_node'

    def get_shortest_path_between_two_nodes(self, source, target):
        if self.topology.node[source]['stack'][0] == 'nfv_node':
            return nx.shortest_path_length(source, target)




class NetworkModelBaseLine:
    """
    Models the internal state of the network.
    This object should never be edited by VNF Allocation Policies directly, but only
    through calls to the network controller.

    """

    def __init__(self, topology, nfv_cache_policy, shortest_path=None):  #

        if not isinstance(topology, fnss.Topology):
            raise ValueError('The topology argument must be an'
                             'instance of fnss.Topology or   of its subclasses')

        self.shortest_path = dict(shortest_path) if shortest_path is not None \
            else (dict(nx.all_pairs_dijkstra_path(topology)))

        self.topology = topology
        self.nfv_cache = None

        self.link_type = nx.get_edge_attributes(topology, 'type')
        self.link_delay = fnss.get_delays(topology)

        if not topology.is_directed():
            for (u, v), link_type in list(self.link_type.items()):
                self.link_type[(v, u)] = link_type

            for (u, v), delay in list(self.link_delay.items()):
                self.link_delay[(v, u)] = delay

        nfv_cache_size = {}
        for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'nfv_node':
                if 'cache_size' in stack_props:
                    nfv_cache_size[node] = stack_props['cache_size']
        if any(c < 8 for c in nfv_cache_size.values()):
            logger.warning('Some nfv node caches have size less than 8.'
                           'I am setting them to 8 and run the experiment anyway')
            for node in nfv_cache_size:
                if nfv_cache_size[node] < 8:
                    nfv_cache_size[node] = 8

        # use when the len(vnfs) < len(nfv_nodes)
        def vnfs_assignment(nfv_nodes, vnfs):
            if len(nfv_nodes) < len(vnfs):
                return dict(zip(cycle(nfv_nodes), vnfs))
            else:
                return dict(zip(nfv_nodes, cycle(vnfs)))

        policy_name = nfv_cache_policy['name']
        # policy_name = 'NFV_CACHE'
        policy_args = {k: v for k, v in nfv_cache_policy.items() if k != 'name'}
        # The actual cache objects storing the vnfs
        self.nfv_cache = {node: CACHE_POLICY[policy_name](nfv_cache_size[node], **policy_args)
                          for node in nfv_cache_size}

        # for node in self.nfv_cache:
        # print(node)
        # self.nfv_cache[node].list_nfv_cache()

        sfcs = [5, 7, 8, 3, 1, 2, 4, 6]
        # sfcs = [[5, 7, 8, 3], [7, 6], [5, 4, 2], [2, 5, 3, 7], [1, 3] ]
        """
        sfcs = [
            [5, 7, 8, 3], [5, 7, 2, 1], [3, 8, 2, 6], [7, 2], [7], [3, 5], [8, 3, 1], [2, 6], [5, 4, 3, 2], [1, 3],
            [2], [6], [4, 3, 7, 1], [8, 6], [6], [3, 1, 4, 7], [2, 8, 6, 3], [8, 6, 2], [6, 4, 2, 8], [1, 4],
            [7, 5, 1, 3], [2, 5, 3, 7], [5, 4, 2], [2, 4, 3, 1], [1], [4, 2, 1, 5], [7, 6], [4, 7, 3, 6],
            [7, 3, 5, 6], [4, 3]
        ]
        """

        # place a single vnf in all nfv-nodes

        target_nfv_nodes = vnfs_assignment(self.nfv_cache, sfcs)
        for node in self.nfv_cache:
            if node in target_nfv_nodes.keys():
                # print(node)
                vnf = target_nfv_nodes[node]
                # for vnf in sfc:
                self.nfv_cache[node].add_vnf(vnf)
                # self.nfv_cache[node].list_nfv_cache()

        """
        target_nfv_nodes = vnfs_assignment(self.nfv_cache, sfcs)
        for node in self.nfv_cache:
            if node in target_nfv_nodes.keys():
                #print(node)
                vnfs = target_nfv_nodes[node]
                for vnf in vnfs:
                    self.nfv_cache[node].add_vnf(vnf)
                    #self.nfv_cache[node].list_nfv_cache()
        
        """

    @staticmethod
    def select_random_vnf():
        vnfs = [1, 2, 3, 4, 5, 6, 7, 8]
        return random.choice(vnfs)

    @staticmethod
    def shortest_path(topology, ingress_node, egress_node):
        return nx.shortest_path(topology, ingress_node, egress_node)

    @staticmethod
    def calculate_all_shortest_paths(topology, ingress_node, egress_node):
        return [p for p in nx.all_shortest_paths(topology, ingress_node, egress_node)]

    @staticmethod
    def get_ingress_nodes(topology):

        if isinstance(topology, fnss.Topology):
            ing_nodes = []
            for node in topology.nodes():
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'ingress_node':
                    ing_nodes.append(node)

            return ing_nodes

    @staticmethod
    def get_egress_nodes(topology):

        if isinstance(topology, fnss.Topology):
            egr_nodes = []
            for node in topology.nodes():
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'egress_node':
                    egr_nodes.append(node)

            return egr_nodes

    @staticmethod
    def get_nfv_nodes(topology):
        return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']

    def get_nfv_nodes_path(self, path):

        nfv_nodes = []
        for node in path:
            if self.topology.node[node]['stack'][0] == 'nfv_node':
                nfv_nodes.append(node)
        return nfv_nodes

    def get_ingress_node_path(self, path):
        for node in path:
            return self.topology.node[node]['stack'][0] == 'ingress_node'

    def get_egress_node_path(self, path):
        for node in path:
            return self.topology.node[node]['stack'][0] == 'egress_node'

    def get_shortest_path_between_two_nodes(self, source, target):
        if self.topology.node[source]['stack'][0] == 'nfv_node':
            return nx.shortest_path_length(source, target)


class NetworkModelFirstOrder:
    """
    Models the internal state of the network.
    This object should never be edited by VNF Allocation Policies directly, but only
    through calls to the network controller.

    """

    def __init__(self, topology, nfv_cache_policy, shortest_path=None):  #

        if not isinstance(topology, fnss.Topology):
            raise ValueError('The topology argument must be an'
                             'instance of fnss.Topology or   of its subclasses')

        self.shortest_path = dict(shortest_path) if shortest_path is not None \
            else (dict(nx.all_pairs_dijkstra_path(topology, weight='delay')))

        self.topology = topology
        self.nfv_cache = None

        self.link_type = nx.get_edge_attributes(topology, 'type')
        self.link_delay = fnss.get_delays(topology)

        if not topology.is_directed():
            for (u, v), link_type in list(self.link_type.items()):
                self.link_type[(v, u)] = link_type

            for (u, v), delay in list(self.link_delay.items()):
                self.link_delay[(v, u)] = delay
                #print(delay)

        nfv_cache_size = {}
        for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'nfv_node':
                if 'cache_size' in stack_props:
                    nfv_cache_size[node] = stack_props['cache_size']
        if any(c < 8 for c in nfv_cache_size.values()):
            logger.warning('Some nfv node caches have size less than 8.'
                           'I am setting them to 8 and run the experiment anyway')
            for node in nfv_cache_size:
                if nfv_cache_size[node] < 8:
                    nfv_cache_size[node] = 8

        # use when the len(vnfs) < len(nfv_nodes)
        def vnfs_assignment(nfv_nodes, vnfs):
            if len(nfv_nodes) < len(vnfs):
                return dict(zip(cycle(nfv_nodes), vnfs))
            else:
                return dict(zip(nfv_nodes, cycle(vnfs)))

        policy_name = nfv_cache_policy['name']
        # policy_name = 'NFV_CACHE'
        policy_args = {k: v for k, v in nfv_cache_policy.items() if k != 'name'}
        # The actual cache objects storing the vnfs
        self.nfv_cache = {node: CACHE_POLICY[policy_name](nfv_cache_size[node], **policy_args)
                          for node in nfv_cache_size}

        # for node in self.nfv_cache:
        # print(node)
        # self.nfv_cache[node].list_nfv_cache()

        first_order_sfcs = [
            [5, 4],
            [4, 6],
            [7, 8],
            [2, 3],
            [3, 5],


        ]

        # place a single vnf in all nfv-nodes

        target_nfv_nodes = vnfs_assignment(self.nfv_cache, first_order_sfcs)
        for node in self.nfv_cache:
            if node in target_nfv_nodes.keys():
                # print(node)
                sfc = target_nfv_nodes[node]
                for vnf in sfc:
                    self.nfv_cache[node].add_vnf(vnf)
                    # self.nfv_cache[node].list_nfv_cache()

        """
        target_nfv_nodes = vnfs_assignment(self.nfv_cache, sfcs)
        for node in self.nfv_cache:
            if node in target_nfv_nodes.keys():
                #print(node)
                vnfs = target_nfv_nodes[node]
                for vnf in vnfs:
                    self.nfv_cache[node].add_vnf(vnf)
                    #self.nfv_cache[node].list_nfv_cache()
        
        """

    @staticmethod
    def select_random_vnf():
        vnfs = [1, 2, 3, 4, 5, 6, 7, 8]
        return random.choice(vnfs)

    @staticmethod
    def shortest_path(topology, ingress_node, egress_node):
        return nx.shortest_path(topology, ingress_node, egress_node)

    @staticmethod
    def calculate_all_shortest_paths(topology, ingress_node, egress_node):
        return [p for p in nx.all_shortest_paths(topology, ingress_node, egress_node)]

    @staticmethod
    def get_ingress_nodes(topology):

        if isinstance(topology, fnss.Topology):
            ing_nodes = []
            for node in topology.nodes():
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'ingress_node':
                    ing_nodes.append(node)

            return ing_nodes

    @staticmethod
    def get_egress_nodes(topology):

        if isinstance(topology, fnss.Topology):
            egr_nodes = []
            for node in topology.nodes():
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'egress_node':
                    egr_nodes.append(node)

            return egr_nodes

    @staticmethod
    def get_nfv_nodes(topology):
        return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']

    def get_nfv_nodes_path(self, path):

        nfv_nodes = []
        for node in path:
            if self.topology.node[node]['stack'][0] == 'nfv_node':
                nfv_nodes.append(node)
        return nfv_nodes

    def get_ingress_node_path(self, path):
        for node in path:
            return self.topology.node[node]['stack'][0] == 'ingress_node'

    def get_egress_node_path(self, path):
        for node in path:
            return self.topology.node[node]['stack'][0] == 'egress_node'

    def get_shortest_path_between_two_nodes(self, source, target):
        if self.topology.node[source]['stack'][0] == 'nfv_node':
            return nx.shortest_path_length(source, target)


################################### NetworkModelHodVnfs ##################################################


class NetworkModelProposal:
    """
    Models the internal state of the network.
    This object should never be edited by VNF Allocation Policies directly, but only
    through calls to the network controller.

    """

    def __init__(self, topology, nfv_cache_policy, shortest_path=None):  #

        if not isinstance(topology, fnss.Topology):
            raise ValueError('The topology argument must be an'
                             'instance of fnss.Topology or   of its subclasses')

        self.shortest_path = dict(shortest_path) if shortest_path is not None \
            else (dict(nx.all_pairs_dijkstra_path(topology)))

        self.nfv_cache = None
        self.topology = topology

        self.link_type = nx.get_edge_attributes(topology, 'type')
        self.link_delay = fnss.get_delays(topology)
    
        if not topology.is_directed():
            for (u, v), link_type in list(self.link_type.items()):
                self.link_type[(v, u)] = link_type

            for (u, v), delay in list(self.link_delay.items()):
                self.link_delay[(v, u)] = delay

        nfv_cache_size = {}
        for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'nfv_node':
                if 'cache_size' in stack_props:
                    # self.nfv_nodes.append(node)
                    nfv_cache_size[node] = stack_props['cache_size']
        if any(c < 8 for c in nfv_cache_size.values()):
            logger.warning('Some nfv node caches have size less than 8. '
                           'I am setting them to 8 and run the experiment anyway')
            for node in nfv_cache_size:
                if nfv_cache_size[node] < 8:
                    nfv_cache_size[node] = 8

        policy_name = nfv_cache_policy['name']
        # policy_name = 'NFV_CACHE'
        policy_args = {k: v for k, v in nfv_cache_policy.items() if k != 'name'}
        # The actual cache objects storing the vnfs
        self.nfv_cache = {node: CACHE_POLICY[policy_name](nfv_cache_size[node], **policy_args)
                          for node in nfv_cache_size}

        def hod_vnfs_assignment(nfv_nodes, sfcs):
            if len(nfv_nodes) < len(sfcs):
                return dict(zip(cycle(nfv_nodes), sfcs))
            else:
                return dict(zip(nfv_nodes, cycle(sfcs)))

        # all hod_vnfs found on the training phase
        hods_vnfs = [
            [6, 2, 3],
            [1, 5, 2, 3],
            [3, 2, 5, 6, 7],
            [2, 5, 8],
            [2, 3, 4, 5],




        ]

        # place vnfs on top-20 nfv_nodes with the highest betweenness_centrality value
        betw_nfv_nodes = NetworkModelProposal.get_top_betw_nodes(topology, 30)
        target_nfv_nodes = hod_vnfs_assignment(betw_nfv_nodes, hods_vnfs)
        for node in self.nfv_cache:
            if node in target_nfv_nodes.keys():
                #print(node)
                vnfs = target_nfv_nodes[node]
                for vnf in vnfs:
                    self.nfv_cache[node].add_vnf(vnf)
                    #self.nfv_cache[node].list_nfv_cache()


        """
        # Place vnfs on all nfv_nodes of the topology
        target_nfv_nodes = hod_vnfs_assignment(self.nfv_cache, hods_vnfs)
        for target_nfv_node in target_nfv_nodes.keys():
            # print(target_nfv_node)
            vnfs = target_nfv_nodes[target_nfv_node]
            for vnf in vnfs:
                self.nfv_cache[target_nfv_node].add_vnf(vnf)
                # self.nfv_cache[target_nfv_node].list_nfv_cacPOLICY_BAR_COLOR_LINK_LOADhe()
        """


        # Place vnfs on the closest nfv_nodes to the egress_nodes
        """
        self.nfv_nodes = NetworkModelProposal.select_nfv_nodes_path(self, topology)
        #print(self.nfv_nodes)
        target_nfv_nodes = hod_vnfs_assignment(self.nfv_nodes, hods_vnfs)
        for node in self.nfv_cache:
            if node in  target_nfv_nodes.keys():
                #print(target_nfv_node)
                vnfs = target_nfv_nodes[node]
                for vnf in vnfs:
                    self.nfv_cache[node].add_vnf(vnf)
                    #self.nfv_cache[target_nfv_node].list_nfv_cache()
        
        """

    @staticmethod
    def get_top_betw_nodes(topology, n_of_nodes):
        dict_nodes_betw = nx.betweenness_centrality(topology)
        ord_dict =  OrderedDict(sorted(dict_nodes_betw.items(), key=itemgetter(1), reverse=True))
        return dict(list(ord_dict.items())[0:n_of_nodes])


    @staticmethod
    def shortest_path_len(topology, source_node, dest_node):
        return nx.shortest_path_length(topology, source_node, dest_node)

    @staticmethod
    def calculate_all_shortest_paths(topology, ingress_node, egress_node):
        return [p for p in nx.all_shortest_paths(topology, ingress_node, egress_node)]

    @staticmethod
    def get_ingress_nodes(topology):
        return [v for v in topology if topology.node[v]['stack'][0] == 'ingress_node']

    @staticmethod
    def get_egress_nodes(topology):
        return [v for v in topology if topology.node[v]['stack'][0] == 'egress_node']

    @staticmethod
    def get_nfv_nodes(topology):
        return [v for v in topology if topology.node[v]['stack'][0] == 'nfv_node']

    @staticmethod
    def get_nfv_nodes_path(topology, path):
        nfv_nodes = []
        for node in path:
            if node in NetworkModelProposal.get_nfv_nodes(topology):
                nfv_nodes.append(node)
        return nfv_nodes

    @staticmethod
    def get_ingress_node_path(topology, path):
        for node in path:
            if node in NetworkModelProposal.get_ingress_nodes(topology):
                return node

    @staticmethod
    def get_egress_node_path(topology, path):
        for node in path:
            if node in NetworkModelProposal.get_egress_nodes(topology):
                return node

    def select_nfv_nodes_path(self, topology):
        path_dist = defaultdict(list)
        dist_nfv_egr = defaultdict(int)
        target_nfv_nodes = []
        ing_nodes = NetworkModelProposal.get_ingress_nodes(topology)
        egr_nodes = NetworkModelProposal.get_egress_nodes(topology)
        for ing_node in ing_nodes:
            for egr_node in egr_nodes:
                path_ing_egr = self.shortest_path[ing_node][egr_node]
                path_dist[ing_node] = path_ing_egr
                nfv_nodes_path = NetworkModelProposal.get_nfv_nodes_path(topology, path_ing_egr)
                for nfv_node_path in nfv_nodes_path:
                    dist_nfv_egr[nfv_node_path] = NetworkModelProposal.shortest_path_len(topology, nfv_node_path,
                                                                                         egr_node)
                    closest_nfv_node = min(dist_nfv_egr, key=lambda k: dist_nfv_egr[k]) if len(dist_nfv_egr) > 0 \
                        else print("No nfv_node found on path")
                    if closest_nfv_node not in target_nfv_nodes:
                        target_nfv_nodes.append(closest_nfv_node)
        return target_nfv_nodes

    def get_closest_nfv_node_path(self, path):
        nfv_nodes = []
        closest_node = None
        dist_nfv_node_egr_node = defaultdict(int)
        egr_node = NetworkModelProposal.get_egress_node_path(self.topology, path)
        for node in path:
            if self.topology.node[node]['stack'][0] == 'nfv_node':
                nfv_nodes.append(node)
        for nfv_node in nfv_nodes:
            dist_nfv_node_egr_node[nfv_node] = len(self.get_shortest_path_between_two_nodes(nfv_node, egr_node))
            closest_node = min(dist_nfv_node_egr_node, key=lambda k: dist_nfv_node_egr_node[k]) if len(
                dist_nfv_node_egr_node) > 0 \
                else None
        return closest_node

    """
    @staticmethod
    def get_closest_nfv_nodes(topology):
        dist_ingress_node_egress_node = defaultdict(int)
        pair_dist = dict(nx.all_pairs_shortest_path_length(topology))
        closest_nfv_nodes = []
        ingress_nodes = NetworkModelProposal.get_ingress_nodes(topology)
        egress_nodes = NetworkModelProposal.get_egress_nodes(topology)
        nfv_nodes_candidates = NetworkModelProposal.get_nfv_nodes(topology)
        for ingress_node in ingress_nodes:
            for egress_node in egress_nodes:
                dist_ingress_node_egress_node[ingress_node] =  NetworkModelProposal.get_shortest_path_between_two_nodes(ingress_node, egress_node)
                closest_nfv_node = min(dist_ingress_node_egress_node,  key=lambda k: dist_nfv_node_egress_node[k])\
            if len(dist_ingress_node_egress_node) > 0 else print("No nfv_node found")
            if closest_nfv_node not in closest_nfv_nodes:
                closest_nfv_nodes.append(closest_nfv_node)
        return closest_nfv_nodes
    """

    def get_shortest_path_between_two_nodes(self, source, target):
        return self.shortest_path[source][target]


class NetworkController:

    def __init__(self, model):

        self.session = None
        self.model = model
        self.collector = None

    def attach_collector(self, collector):
        self.collector = collector

    def detach_collector(self):
        self.collector = None

    def start_session(self, timestamp, sfc_id, ingress_node, egress_node, sfc, delay, log):
        self.session = dict(timestamp=timestamp,
                            ingress_node=ingress_node,
                            egress_node=egress_node,
                            sfc=sfc,
                            delay=delay,
                            log=log)

        if self.collector is not None and self.session['log']:
            self.collector.start_session(timestamp, sfc_id, ingress_node, egress_node, sfc, delay)

    def forward_request_path(self, ingress_node, egress_node, path=None, main_path=True):

        if path is None:
            path = self.model.shortest_path[ingress_node][egress_node]
        for u, v in path_links(path):
            self.forward_request_vnf_hop(u, v, main_path)

    def forward_request_vnf_hop(self, u, v, main_path=True):

        if self.collector is not None and self.session['log']:
            self.collector.request_vnf_hop(u, v, main_path)

    def proc_vnf_payload(self, u, v, main_path=True):
        if self.collector is not None and self.session['log']:
            self.collector.vnf_proc_payload(u, v, main_path)

    def vnf_proc(self, vnf):
        if self.collector is not None and self.session['log']:
            self.collector.vnf_proc_delay(vnf)

    def get_vnf(self, node, vnf):
        if node in self.model.nfv_cache:
            has_vnf = self.model.nfv_cache[node].get_vnf(vnf)
            if has_vnf:
                return True
            else:
                return False

    def sfc_hit(self, sfc_id):
        if self.collector is not None and self.session['log']:
            self.collector.sfc_hit(sfc_id)

    def get_delay_sfc(self):
        if self.collector is not None and self.session['log']:
            self.collector.get_sess_latency()


    def put_vnf(self, node, vnf):
        if node in self.model.nfv_cache:
            return self.model.nfv_cache[node].add_vnf(vnf)

    def put_sfc(self, node, sfc):
        if node in self.model.nfv_cache:
            for vnf in sfc:
                self.model.nfv_cache[node].add_vnf(vnf)

    def get_closest_nfv_node(self, path):
        return self.model.get_closest_nfv_node_path(path)


    def sum_vnfs_cpu_on_node(self, node):
        if node in self.model.nfv_cache:
            return self.model.nfv_cache[node].sum_vnfs_cpu_node()

    def nodes_used_cpu(self, path):
        dict_nodes_cpu_used = {}
        for node in path:
            dict_nodes_cpu_used[node] = self.sum_vnfs_cpu_on_node(node)
        return dict_nodes_cpu_used

    def path_capacity_rem_cpu(self, path):
        dict_cpu_nodes = self.nodes_used_cpu(path)
        return sum(dict_cpu_nodes.values())



    def find_nfv_node_with_min_cpu_alloc(self, source, target):
        path = self.model.shortest_path[source][target]
        target_node = min(self.sum_vnfs_cpu_on_node(node) for node in path if node in self.model.nfv_cache)
        return target_node

    def end_session(self, success=True):

        if self.collector is not None and self.session['log']:
            self.collector.end_session(success)
        self.session = None
