import networkx as nx
import fnss
import random
from nfvpysim.registry import CACHE_POLICY
from nfvpysim.util import path_links
import logging
logger = logging.getLogger('orchestration')

from nfvpysim.scenarios import topology_geant


__all__ = [
    'NetworkModel',
    'NetworkView',
    'NetworkController'
]


class NetworkView:

    def __init__(self, model):

        if not isinstance(model, NetworkModel):
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



class NetworkModel:
    """
    Models the internal state of the network.
    This object should never be edited by VNF Allocation Policies directly, but only
    through calls to the network controller.

    """

    def __init__(self,topology, nfv_cache_policy , shortest_path=None): #


        if not isinstance(topology, fnss.Topology):
            raise ValueError('The topology argument must be an'
                             'instance of fnss.Topology or   of its subclasses')

        self.shortest_path = dict(shortest_path) if shortest_path is not None \
            else (dict(nx.all_pairs_dijkstra_path(topology)))


        self.topology = topology

        self.dict_vnfs_cpu_req_proc_delay = {1: 15,   # nat
                                             2: 25,   # fw
                                             3: 25,   # ids
                                             4: 20,   # wanopt
                                             5: 20,   # lb
                                             6: 25,   # encrypt
                                             7: 25,   # decrypt
                                             8: 25,   # decrypt
                                  }


        self.link_type = nx.get_edge_attributes(topology, 'type')
        self.link_delay = fnss.get_delays(topology)

        if not topology.is_directed():
            for (u,v), link_type in list(self.link_type.items()):
                self.link_type[(v,u)] = link_type

            for (u,v), delay in list(self.link_delay.items()):
                self.link_delay[(v,u)] = delay

        nfv_cache_size = {}
        for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'nfv_node':
                if 'cache_size' in stack_props:
                    nfv_cache_size[node] = stack_props['cache_size']
        if any(c < 8 for c in nfv_cache_size.values()):
            logger.warning('Some nfv node caches have size less than 8. '
                        'I am setting them to 8 and run the experiment anyway')
            for node in nfv_cache_size:
                if nfv_cache_size[node] < 8:
                    nfv_cache_size[node] = 8



        policy_name = nfv_cache_policy['name']
        policy_args = {k: v for k, v in nfv_cache_policy.items() if k != 'name'}
        # The actual cache objects storing the vnfs
        self.nfv_cache = {node: CACHE_POLICY[policy_name](nfv_cache_size[node], **policy_args)
                                  for node in nfv_cache_size}

        for node in self.nfv_cache:
            #vnfs = NetworkModel.var_len_seq_sfc()
            vnfs = NetworkModel.select_random_sfc()
            for vnf in vnfs:
                self.nfv_cache[node].add_vnf(vnf)


    # Method to allocate statically a random sfc on an nfv cache node
    @staticmethod
    def select_random_sfc():
        services = [
            [1, 2],  # [nat - fw]
            [4, 5],  # [wanopt - lb]
            [1, 2, 3],  # [nat - fw - ids]
            [2, 3, 5],  # [fw - ids - lb]
            [1, 5, 4],  # [nat - lb - wanopt]
            [5, 2, 1],  # [lb - fw - nat]
            [2, 3, 5, 6],  # [fw - ids - lb - encrypt]
            [3, 2, 5, 8],  # [ids - fw - lb - wanopt]
            [5, 4, 6, 2, 3],  # [lb - wanopt - encrypt - fw - ids]
        ]
        return random.choice(services)

    # Method to generate a variable-length sfc in order to be allocated on an nfv cache node
    @staticmethod
    def var_len_seq_sfc():
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
                sfc_len -= 1
                sum_cpu += cpu
                if sum_cpu > 100 or sfc_len == 0:
                    break
                elif sum_cpu <= 100 and sfc_len != 0:
                    sfc_len -= 1

        return var_len_sfc

    # Compute the shortest path between ingress and egress node
    @staticmethod
    def shortest_path(topology, ingress_node, egress_node):
        return nx.shortest_path(topology, ingress_node,egress_node)


    @staticmethod
    def calculate_all_shortest_paths(topology, ingress_node, egress_node):
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




    def get_ingress_node_path(self, path):
        for node in path:
            return self.topology.node[node]['stack'][0] == 'ingress_node'


    def get_egress_node_path(self, path):
        for node in path:
            return self.topology.node[node]['stack'][0] == 'egress_node'



    def get_shortest_path_between_two_nodes(self, source, target):
        if self.topology[source]['stack'][0] == 'nfv_node':
            return nx.shortest_path_length(source, target)




class NetworkController:

    def __init__(self, model):

        self.session = None
        self.model = model
        self.collector = None


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



    def forward_request_path(self, ingress_node, egress_node, path=None, main_path=True):

        if path is None:
            path = self.model.shortest_path[ingress_node][egress_node]
        for u, v in path_links(path):
            self.forward_request_vnf_hop(u, v, main_path)



    def forward_request_vnf_hop(self, u, v, main_path=True):

        if self.collector is not None and self.session['log']:
            self.collector.request_vnf_hop(u, v, main_path)


    def forward_vnf_hop(self, u, v, main_path=True):

        if self.collector is not None and self.session['log']:
            self.collector.vnf_proc_hop(u, v, main_path)


    def vnf_proc(self, vnf):

        if self.collector is not None and self.session['log']:
            self.collector.vnf_proc_delay(vnf)


    def get_vnf(self, node, vnf):
        if node in self.model.nfv_cache:
            vnf_hit = self.model.nfv_cache[node].get_vnf(vnf)
            if vnf_hit:
                if self.session['log']:
                    self.collector.vnf_hit(vnf)
            return vnf_hit




    def put_vnf(self, node, vnf):
        if node in self.model.nfv_cache:
            return self.model.nfv_cache[node].add_vnf(vnf)


    def put_sfc(self, node, sfc):
        if node in self.model.nfv_cache:
            for vnf in sfc:
                self.model.nfv_cache[node].add_vnf(vnf)







    def get_vnf_path_without_vnf_placement(self, ingress_node, egress_node, sfc):
        vnf_status = {}
        path = self.model.shortest_path[ingress_node][egress_node]
        for node in path:
            if node in self.model.cache:
                for vnf in sfc:
                    vnf_status = {vnf: False for vnf in sfc}
                    if self.get_vnf(node, vnf) and vnf_status[vnf] == False: # vnf on node and processed
                        vnf_status[vnf] = True
                        continue
                    elif self.get_vnf(node, vnf) and vnf_status[vnf] == True: # vnf has already been processed in previous node
                        continue
                    elif not self.get_vnf(node, vnf): # vnf not on node and not processed yet
                        continue
        if all(value == True for value in vnf_status.values()):
            if self.collector is not None and self.session['log']:
                self.collector.sfc_acc(sfc)
            return True
        else:
            return False



    def get_vnf_path_with_vnf_placement(self, ingress_node, egress_node, sfc):
        vnf_status = {}
        missed_vnfs = []
        path = self.model.shortest_path[ingress_node][egress_node]
        for node in path:
            if node in self.model.cache:
                for vnf in sfc:
                    vnf_status = {vnf: False for vnf in sfc}
                    if self.get_vnf(node, vnf) and vnf_status[vnf] == False: # vnf on node and processed
                        vnf_status[vnf] = True
                        continue
                    elif self.get_vnf(node, vnf) and vnf_status[vnf] == True: # vnf has already been processed in previous node
                        continue
                    elif not self.get_vnf(node, vnf): # vnf not on node and not processed yet
                        missed_vnfs.append(vnf)
                        continue



        if all(value == True for value in vnf_status.values()):
            if self.collector is not None and self.session['log']:
                self.collector.sfc_acc(sfc)
            return True
        else:
            return False



    def get_closest__nfv_node(self, path):
        dist_nfv_node_egress_node = {}
        egress_node = self.model.get_egress_nodes(path)
        nfv_nodes_candidates = self.model.get_nfv_nodes(path)
        for nfv_node in nfv_nodes_candidates:
            dist_nfv_node_egress_node[nfv_node] = self.model.get_shortest_path_between_two_nodes(nfv_node, egress_node)
        closest_nfv_node = min(dist_nfv_node_egress_node.values())
        return closest_nfv_node


    def sum_cpu_req_vnfs(self, vnfs):
        return sum(vnf.values() for vnf in vnfs)


    def sum_vnfs_cpu_node(self, node):
        return self.model.cache[node].get_sum_vnfs_cpu()



    def find_target_nfv_node(self, path, vnfs):
        target_node = min(self.sum_vnfs_cpu_node(node) for node in path \
                          if self.sum_vnfs_cpu_node(node) <= self.sum_cpu_req_vnfs(vnfs))

        return target_node


    def end_session(self, success=True):

        if self.collector is not None and self.session['log']:
            self.collector.end_session(success)
        self.session = None

