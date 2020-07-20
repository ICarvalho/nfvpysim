import random
import networkx as nx
from tools.stats import TruncatedZipfDist
from topologies.topology import topology_tatanld
from model.request import *


class StationaryWorkload:

    """
    This function generates events on the fly, i.e. instead of creating an
    event schedule to be kept in memory, returns an iterator that generates
    events when needed.

    This is useful for running large schedules of events where RAM is limited
    as its memory impact is considerably lower

    All requests are mapped to receivers uniformly unless a positive *beta*
    parameter is specified


    """

    def __init__(self, topology, rate=1.0, n_req=10**3, seed=None, **kwargs):

        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.egress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'egress_node']
        self.rate = rate
        self.n_req = n_req
        random.seed(seed)


    def __iter__(self):
        req_counter = 0
        t_event = 0.0
        while req_counter < self.n_req:
            t_event += (random.expovariate(self.rate))
            ingress_node = random.choice(self.ingress_nodes)
            egress_node = random.choice(self.egress_nodes)
            sfc = RequestRandomSfc().get_sfc()
            log = (req_counter <= self.n_req)
            event = {'ingress_node': ingress_node, 'egress_node': egress_node, 'sfc': sfc, 'log': log}
            yield (t_event, event)
            req_counter += 1
        raise StopIteration()



topo = topology_tatanld()
print(len(topo.nodes()))
workload = StationaryWorkload(topo)
for i in workload:
    print(i)

