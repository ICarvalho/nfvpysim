import networkx as nx
import fnss
from topologies.topology import topology_geant, topology_datacenter_two_tier, topology_tatanld
import random
from model.request import *
from model.nodes import *
from model.vnfs import *


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


    def all_pairs_shortest_paths(self, ingress_node, egress_node):
        return  self.model.calculate_all_shortest_paths[ingress_node][egress_node]


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

    def __init__(self, topology): #, policy, shortest_path=None):

        if not isinstance(topology, fnss.Topology):
            raise ValueError('The topology argument must be an'
                             'instance of fnss.Topology or any of its subclasses')

       # self.shortest_path = shortest_path if shortest_path is not None \
                           #  else symmetrify_paths(nx.all_pairs_dijkstra_path(topology))
        self.topology = topology
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

        for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'ingress_node':
                if 'id' in stack_props:
                    self.ingress_nodes[node] = stack_props['id']
            elif stack_name == 'egress_node':
                if 'id' in stack_props:
                    self.egress_nodes[node] = stack_props['id']
            elif stack_name == 'nfv_node':
                if 'id' in stack_props:
                    if 'cpu' in stack_props:
                        if 'ram' in stack_props:
                            if 'r_cpu' in stack_props:
                                if 'r_ram' in stack_props:
                                    if 'vnfs' in stack_props:
                                        self.nfv_nodes[node] = stack_props['id']
                                        self.nfv_nodes[node] = stack_props['cpu']
                                        self.nfv_nodes[node] = stack_props['ram']
                                        self.nfv_nodes[node] = stack_props['r_cpu']
                                        self.nfv_nodes[node] = stack_props['r_ram']
                                        self.nfv_nodes[node] = stack_props['vnfs']
            elif stack_name == 'fw_node':
                self.fw_nodes[node] = stack_props['id']




       # policy_name = policy['name']
        #policy_args = {k: v for k, v in policy.items() if k != 'name'}



    # Compute the shortest path between ingress and egress node
    def calculate_shortest_path(self, topology, ingress_node, egress_node):
        return nx.shortest_path(topology, ingress_node,egress_node)


    def calculate_all_shortest_paths(self, topology, ingress_node, egress_node):
        return [p for p in nx.all_shortest_paths(topology, ingress_node, egress_node)]




    # Select the ingress node to send the VNFs request
    def list_ingress_nodes(self, topology):


        ingress_nodes_candidates = []
        for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'ingress_node':
               ingress_nodes_candidates.append(node)

        return ingress_nodes_candidates





    # select randomly an ingress node from the ones available in list_ingress_nodes()
    def select_random_ingress_node(self, topology):
        nodes = self.list_ingress_nodes(topology)
        rand_ing_node = random.choice(nodes) if len(nodes) > 0 else None
        return rand_ing_node





    # Select the egress node, where the service is finished
    def list_egress_nodes(self, topology):

        if not isinstance(topology, fnss.Topology):
            raise ValueError('The provided topology must be an instance of'
                             'fnss.Topology or any of its subclasses')

        egress_nodes_candidates = []
        for node in topology.nodes:
            stack_name, stack_props= fnss.get_stack(topology, node)
            if stack_name == 'egress_node':
                egress_nodes_candidates.append(node)

        return egress_nodes_candidates

    # select randomly an ingress node from the ones available in list_ingress_nodes()
    def select_random_egress_node(self, topology):
        nodes = self.list_egress_nodes(topology)
        rand_egr_node = random.choice(nodes) if len(nodes) > 0 else None
        return rand_egr_node




    
    
    def proc_request_path(self, request, path):

        vnf_proc = {vnf: False for vnf in request}
        for node in path:
            if isinstance(node, VnfNode):
                for vnf in request:
                    if vnf in node._vnfs and vnf_proc[vnf]:
                        vnf_cpu = getattr(vnf, 'cpu')
                        node.proc_vnf_cpu(vnf_cpu)
                        vnf_proc[vnf] = True


        return vnf_proc





    #return all vnf nodes along a given path
    def get_vnf_nodes_path(self, topology,  path):
        list_vnf_nodes = []
        for node in path:
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'nfv_node':
                list_vnf_nodes.append(node)

        return list_vnf_nodes



    # Convert a path expressed as list of nodes into a path expressed as a list of edges.
    def path_links(self, path):

        return [(path[i], path[i + 1]) for i in range(len(path) - 1)]



################################### END OF NETWORK MODEL ###################################################



class NetworkController:

    def __init__(self, model):

        self.session = None
        self.model = model
        self.collector = None

    def attach_collector(self, collector):
        self.collector = collector


    def detach_collector(self):
        self.collector = None


    def start_session(self, timestamp, ingress_node, request, log):
        self.session = dict(timestamp=timestamp,
                            receiver=ingress_node,
                            request=request,
                            log=log)

        if self.collector is not None and self.session['log']:
            self.collector.start_session(timestamp, ingress_node, request)

    def forward_request_path(self, s, t, path=None, main_path=True):

        if path is None:
            path = self.model.shortest_path[s][t]
        for u, v in NetworkModel.path_links(path):
            self.forward_request_hop(u, v, main_path)

    def forward_request_hop(self, u, v, main_path=True):

        if self.collector is not None and self.session['log']:
            self.collector.request_hop(u, v, main_path)


    def end_session(self, success=True):

        if self.collector is not None and self.session['log']:
            self.collector.end_session(success)
        self.session = None

topo = topology_geant()

model = NetworkModel(topo)
view = NetworkView(model)
contr = NetworkController(model)






req_01  = Request()
req = req_01.get_random_sfc()
ingress = view.model.select_random_ingress_node(topo)
egress = view.model.select_random_egress_node(topo)
path = view.model.calculate_shortest_path(topo, ingress, egress)

nat = Nat()
fw = Firewall()
en = Encrypter()
lb = LoadBalancer()

vnfs = [nat, fw, en, lb]

pl =  view.model.uniform_vnf_placement(topo, vnfs, seed=None)



proc = view.model.proc_request_path(req, path)

""" 
print(path)
print(topo.nfv_nodes())
print(topo.ingress_nodes())
print(topo.egress_nodes())
"""
print(topo.nfv_nodes())
print()
print(topo._node)


"""
print(path)
print(req)
print(proc)
"""


