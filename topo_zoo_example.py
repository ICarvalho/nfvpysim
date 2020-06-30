import fnss
import networkx as nx

topology = fnss.parse_topology_zoo(path='/home/igor/PycharmProjects/TESE/datasets/TataNld.graphml').to_undirected()

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
    fnss.add_stack(topology, v, 'ingress_node')

for v in vnf_nodes:
    fnss.add_stack(topology, v, 'vnf_node')

for v in egress_nodes:
    fnss.add_stack(topology, v, 'egress_node')




print(topology.size())
print()
print(len(ingress_nodes))
print()
print(len(vnf_nodes))
print()
print(len(forwarding_nodes))
print()
print(len(egress_nodes))
