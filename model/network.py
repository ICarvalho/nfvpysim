import networkx as nx
import fnss
from topologies.topology import topology_geant, topology_datacenter_two_tier, topology_tatanld
import random
from model.request import *
from model.nodes import *


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


        """
                for node in topology.nodes():
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'ingress_node':
                if 'id' in stack_props:
                    self.ingress_nodes[node] = stack_props['id']

            elif stack_name == 'egress_node':
                if 'id' in stack_props:
                    self.egress_nodes[node] = stack_props['id']

            elif stack_name == 'nfv_node':
                if 'node_specs' in stack_props:
                    self.nfv_nodes[node] = stack_props['node_specs']


            elif stack_name == 'fw_node':
                self.fw_nodes[node] = stack_props['id']
        
        """





    # Compute the shortest path between ingress and egress node
    def calculate_shortest_path(self, topology, ingress_node, egress_node):
        return nx.shortest_path(topology, ingress_node,egress_node)


    def calculate_all_shortest_paths(self, topology, ingress_node, egress_node):
        return [p for p in nx.all_shortest_paths(topology, ingress_node, egress_node)]



    # Convert a path expressed as list of nodes into a path expressed as a list of edges.
    def path_links(self, path):
        return [(path[i], path[i + 1]) for i in range(len(path) - 1)]




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


    def get_nfv_nodes(self, topology):

        if isinstance(topology, fnss.Topology):
            nfv_nodes = []
            for node in topology.nodes():
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'nfv_node':
                    nfv_nodes.append(node)

            return nfv_nodes



    def select_ingress_node(self, topology):
        return random.choice(self.get_ingress_nodes(topology))



    def select_egress_node(self, topology):
        return random.choice(self.get_egress_nodes(topology))




    def get_rem_cpu_path(self, topology, path):
        node_rem_cpu = {}
        for node in path:
            stack_name, stack_props = fnss.get_stack(topology, node)
            if stack_name == 'nfv_node':
                if isinstance(node, VnfNode) and node in self.nfv_nodes:
                    node_rem_cpu[node] = node.get_rem_cpu()

        return node_rem_cpu






    def find_node_max_av_cpu_path(self, topology, path):

        path_nodes = self.get_rem_cpu_path(topology, path)
        node_max_cpu = max(path_nodes.values())
        return node_max_cpu




    def proc_req_greedy(self, topology, request, path):

        for node in path:
            if isinstance(request, (RequestRandomSfc, RequestVarLenSFc)):
                vnfs = request.get_sfc()
                is_proc = {vnf:False for vnf in vnfs}
                stack_name, stack_props = fnss.get_stack(topology, node)
                if stack_name == 'nfv_node':
                    aux_nfv_node = VnfNode()
                    for vnf in vnfs:
                        if vnf in  topology.node[node]['stack'][1]['node_specs']['vnfs']:
                            topology.node[node]['stack'][1]['node_specs']['node_type'] = aux_nfv_node.proc_vnf(vnf)
                            print(aux_nfv_node.get_rem_cpu())





    def show_nfv_nodes_specs(self):

        for node in self.nfv_nodes:
            print(self.nfv_nodes[node])





    
    """
        def proc_request_path(self, topology, request, path):

        if not isinstance(topology, fnss.Topology):
            raise ValueError('The provided topology must be an instance of'
                             'fnss.Topology or any of its subclasses')

        else:

            sum_vnfs_cpu = self.sum_vnfs_cpu(request.get_sfc())
            path_nodes = defaultdict(dict)
            for node in path:
                stack_name, stack_props = fnss.get_stack(topo, node)
                if stack_name == 'nfv_node':
                    if isinstance(node, VnfNode):
                        if sum_vnfs_cpu > node.get_cpu():
                            raise ValueError('The vnfs cannot be processed at one node')

                        elif sum_vnfs_cpu <= node.get_cpu():
                            vnfs = {vnf: vnf.get_cpu() for vnf in request.get_sfc()}
                            max_val_cpu = max(vnfs.values())
                            print(max_val_cpu)


                        #max_vnfs_desc_cpu =print(rem) vnfs.sort(reverse=True)
                            for vnf in request.get_sfc():
                                vnf_cpu = getattr(vnf, 'cpu')[v for v in topology if  topology.node[v]['stack'][0] == 'ingress_node']
                                #vnf_ram = getattr(vnf, 'ram')
                                path_nodes[node]['node']=  node
                                path_nodes[node]['proc_vnf']=  VnfNode().proc_vnf_cpu(vnf_cpu)
                                path_nodes[node]['r_cpu'] = VnfNode().get_rem_cpu()



                                #path_nodes[node]['ram'] = nfv_node.load_vnf_ram(vnf_ram)
                                #path_nodes[node]['ram'] = nfv_node.get_rem_ram()


                return  path_nodes


    
    """



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

ingress = view.model.select_ingress_node(topo)
egress = view.model.select_egress_node(topo)

path = view.model.calculate_shortest_path(topo, ingress, egress)
all_path = view.model.calculate_all_shortest_paths(topo, ingress, egress)

req = RequestRandomSfc()


vnfs = [Nat(), Firewall(), Encrypter()]


print(path)
print(view.model.proc_req_greedy(topo, req, path))

#print(view.model.nfv_nodes)





"""

topo = topology_geant()
model = NetworkModel(topo)
view = NetworkView(model)

print(view.model.nfv_nodes)
print(topo.nfv_nodes())

"""




#print(view.model.get_ingress_nodes(topo))
#print(view.model.select_ingress_node(topo))

#proc = view.model.proc_request_path(topo, req, path)



#nfv_path = view.model.loc  ate_vnf_nodes_path(topo, path)


#print(path)
#print(rem)
#print(topo.nfv_nodes())
#print(all_path)
#print(topo.nfv_nodes())
#print(proc)

