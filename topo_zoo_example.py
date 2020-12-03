import fnss
import networkx as nx

topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/datasets/Geant2012.gml').to_undirected()

deg = nx.degree(topology)

ingress_nodes = [v for v in topology.nodes() if deg[v] ==2]
vnf_nodes = [v for v in topology.nodes() if deg[v] == 3]
egress_nodes = [v for v in topology.nodes() if deg[v] ==1]
forwarding_nodes = [v for v in topology.nodes() if v not in ingress_nodes + vnf_nodes + egress_nodes]

# set weights and delays on links
fnss.set_weights_constant(topology, 1.0)
fnss.set_delays_constant(topology, 2, 'ms')

# Deploy stacks on nodes

for v in ingress_nodes:
    fnss.add_stack(topology, v, 'ingress_node', {'id': '1', 'name': 'vnf_ing_node'})

for v in vnf_nodes:
    fnss.add_stack(topology, v, 'vnf_node', {'id': '2', 'name': 'vnf_nfv_node'})

for v in egress_nodes:
    fnss.add_stack(topology, v, 'egress_node', { 'id': '3', 'name': 'vnf_egr_node'})

for v in forwarding_nodes:
    fnss.add_stack(topology, v, 'forwarding_node', { 'id': '4', 'name': 'vnf_fw_node'})




print(topology.size())
print(len(ingress_nodes))
print(len(vnf_nodes))
print(len(forwarding_nodes))
print(len(egress_nodes))


for node in topology.nodes:
    stack_name, stack_props = fnss.get_stack(topology, node)
    print(topology.node[node]['stack'][1])