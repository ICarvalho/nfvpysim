import networkx as nx
import fnss
from nfvpysim.registry import CACHE_POLICY
from nfvpysim.model.request import *
from nfvpysim.util import path_links
import logging
from collections import defaultdict
logger = logging.getLogger('orchestration')

def symmetrify_paths(shortest_paths):
    """Make paths symmetric

    Given a dictionary of all-pair shortest paths, it edits shortest paths to
    ensure that all path are symmetric, e.g., path(u,v) = path(v,u)

    Parameters
    ----------
    shortest_paths : dict of dict
        All pairs shortest paths

    Returns
    -------
    shortest_paths : dict of dict
        All pairs shortest paths, with all paths symmetric

    Notes
    -----
    This function modifies the shortest paths dictionary provided
    """
    for u in shortest_paths:
        for v in shortest_paths[u]:
            shortest_paths[u][v] = list(reversed(shortest_paths[v][u]))
    return shortest_paths


class NetworkView:

    def __init__(self, model):

        if not isinstance(model, NetworkModel):
            raise ValueError('The model argument must be an instance of '
                             'NetworkModel')

        self.model = model


    def shortest_path(self, ingress_node, egress_node):
        return self.model.calculate_shortest_path[ingress_node][egress_node]


    """
    def vnf_location(self, vnf):
        loc = set(v for v in self.model.cache if self.model.cache[v].has(vnf))
        source = self.vnf_source(vnf)
        if source:
            loc.add(source)
        return loc


    def vnf_source(self, vnf):
        return self.model.vnf_source.get(vnf, None)

    """



    def all_pairs_shortest_paths(self):
        return self.model.shortest_path


    def link_type(self, u, v):
        return self.model.link_type[(u, v)]


    def link_delay(self, u, v):
        return self.model.link_delay[(u, v)]


    def topology(self):
        return self.model.topology


    def vnf_lookup(self, node, vnf):
        if node in self.model.cache:
            return self.model.cache[node].has(vnf)

    def vnf_dumps(self, node):
        if node in self.model.cache:
            return self.model.cache[node].dump()




class NetworkModel:
    """
    Models the internal state of the network.
    This object should never be edited by VNF Allocation Policies directly, but only
    through calls to the network controller.

    """

    def __init__(self, topology, cache_policy, shortest_path=None): #, policy, shortest_path=None):

        self.cache = None
        if not isinstance(topology, fnss.Topology):
            raise ValueError('The topology argument must be an'
                             'instance of fnss.Topology or any of its subclasses')

        self.shortest_path = dict(shortest_path) if shortest_path is not None \
                            else symmetrify_paths(nx.all_pairs_dijkstra_path(topology))


        self.topology = topology

        # dict of location of vnfs  keyed by vnf ID
        self.vnf_source = {}

        # Dictionary mapping the reverse, i.e. nodes to set of vnfs stored
        self.source_vnf = {}

        self.ingress_nodes = {}
        self.egress_nodes = {}
        self.nfv_nodes = {}
        self.fw_nodes = {}

        self.link_type = nx.get_edge_attributes(topology, 'type')
        self.link_delay = fnss.get_delays(topology)

        if not topology.is_directed():
            for (u,v), link_type in list(self.link_type.items()):
                self.link_type[(v,u)] = link_type

            for (u,v), delay in list(self.link_delay.items()):
                self.link_delay[(v,u)] = delay


        nfv_nodes = {}
        for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'ingress_node':
                if 'id' in stack_props:
                    self.ingress_nodes[node] = stack_props['id']

            elif stack_name == 'egress_node':
                if 'id' in stack_props:
                    self.egress_nodes[node] = stack_props['id']

            elif stack_name == 'nfv_node':
                if 'n_vnfs' in stack_props:
                    nfv_nodes[node] = stack_props['n_vnfs']


            elif stack_name == 'fw_node':
                self.fw_nodes[node] = stack_props['id']





        policy_name = cache_policy['name']
        policy_args = {k: v for k, v in cache_policy.items() if k != 'name'}
        # The actual cache objects storing the content
        self.nfv_enabled_nodes = {node: CACHE_POLICY[policy_name](nfv_nodes[node], **policy_args)
                      for node in nfv_nodes}



    # Compute the shortest path between ingress and egress node
    def calculate_shortest_path(self, topology, ingress_node, egress_node):
        return nx.shortest_path(topology, ingress_node,egress_node)


    def calculate_all_shortest_paths(self, topology, ingress_node, egress_node):
        return [p for p in nx.all_shortest_paths(topology, ingress_node, egress_node)]


    def get_ingress_nodes(self, topology):

        if isinstance(topology, fnss.Topology):
            ing_nodes = []
            for node in topology.nodes():
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'ingress_node':
                    ing_nodes.append(node)

            return ing_nodes

    def get_egress_nodes(self, topology):

        if isinstance(topology, fnss.Topology):
            egr_nodes = []
            for node in topology.nodes():
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'egress_node':
                    egr_nodes.append(node)

            return egr_nodes



    def get_nfv_nodes(self, path):

        nfv_nodes = []
        for node in path:
            if self.topology.node[node]['stack'][0] == 'nfv_node':
                    nfv_nodes.append(node)
        return nfv_nodes



    def select_ingress_node(self, topology):
        return random.choice(self.get_ingress_nodes(topology))


    def select_egress_node(self, topology):
        return random.choice(self.get_egress_nodes(topology))



    def get_shortest_path_between_two_nodes(self, source, target):
        if self.topology[source]['stack'][0] == 'nfv_node':
            return nx.shortest_path_length(source, target)







class NetworkController:

    def __init__(self, model):

        self.session = None
        self.model = model
        self.collector = None
        self.dict_vnfs_cpu_req = {1: 15,  # nat
                                  2: 25,  # fw
                                  3: 25,  # ids
                                  4: 20,  # wanopt
                                  5: 20,  # lb
                                  6: 25,  # encrypt
                                  7: 25   # decrypt
                                 }

    def attach_collector(self, collector):
        self.collector = collector


    def detach_collector(self):
        self.collector = None


    def start_session(self, timestamp, ingress_node, egress_node,  sfc, log):
        self.session = dict(timestamp=timestamp,
                            ingress_node=ingress_node,
                            egress_node=egress_node,
                            sfc=sfc,
                            log=log)

        if self.collector is not None and self.session['log']:
            self.collector.start_session(timestamp, ingress_node, egress_node, sfc)
            self.sfc_status[sfc] = {vnf: False for vnf in sfc}



    def forward_request_path(self, ingress_node, egress_node, path=None, main_path=True):

        if path is None:
            path = self.model.shortest_path[ingress_node][egress_node]
        for u, v in path_links(path):
            self.forward_request_hop(u, v, main_path)



    def forward_request_hop(self, u, v, main_path=True):

        if self.collector is not None and self.session['log']:
            self.collector.request_hop(u, v, main_path)



    def get_vnf(self, node, vnf):

        if node in self.model.cache:
            vnf_hit = self.model.cache[node].get_vnf(self.session)[vnf]
            if vnf_hit:
                return True
            else:
                return False


    def get_vnf_path(self, path, sfc):
        vnf_status = {}
        missed_vnfs = []
        for node in path:
            if node in self.model.cache:
                for vnf in sfc:
                    vnf_status = {vnf: False for vnf in sfc}
                    if self.get_vnf(node, vnf) and vnf_status[vnf] == False: # vnf on node and processed
                        vnf_status[vnf] = True
                    elif self.get_vnf(node, vnf) and vnf_status[vnf] == True: # vnf has already been processed in previous node
                        continue
                    elif not self.get_vnf(node, vnf) and vnf_status[vnf] == False: # vnf not on node and not processed yet
                        missed_vnfs.append(vnf)
                        continue
                    break
            for missed_vnf in missed_vnfs:
                if self.get_vnf(node, missed_vnf):
                    vnf_status[missed_vnf] = True
                else:
                    continue

        if all(value == True for value in vnf_status.values()):
                if self.collector is not None and self.session['log']:
                    self.collector.sfc_acc(sfc)
                return True
        else:
            return False



    def get_target_nfv_node(self, ingress_node, egress_node):

        dist_nfv_node_egress_node = {}
        path = self.model.shortest_path[ingress_node][egress_node]
        nfv_nodes_candidates = self.model.get_nfv_nodes(path)
        for nfv_node in nfv_nodes_candidates:
            dist_nfv_node_egress_node[nfv_node] = self.model.get_shortest_path_between_two_nodes(nfv_node, egress_node)
        closest_nfv_node = min(dist_nfv_node_egress_node.values())
        return closest_nfv_node


    def sum_cpu_req_sfc(self, sfc):
        return sum(sfc.values())


    def sum_vnfs_cpu_node(self, node):
        return self.model.cache[node].get_sum_vnfs_cpu()



    def first_fit(self, path, sfc):
        target_node = min(self.sum_vnfs_cpu_node(node) for node in path \
                    if self.sum_vnfs_cpu_node(node) <= self.sum_cpu_req_sfc(sfc))

        return target_node








    def end_session(self, success=True):

        if self.collector is not None and self.session['log']:
            self.collector.end_session(success)
        self.session = None
