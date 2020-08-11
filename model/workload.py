import random
import networkx as nx
from tools.stats import TruncatedZipfDist
from topologies.topology import topology_tatanld
from model.request import *


class StationaryWorkloadRandomSfc:

    """
    This function generates events on the fly, i.e. instead of creating an
    event schedule to be kept in memory, returns an iterator that generates
    events when needed.

    This is useful for running large schedules of events where RAM is limited
    as its memory impact is considerably lower

    All requests are mapped to receivers uniformly unless a positive *beta*
    parameter is specified


    """

    def __init__(self, topology,  rate=1.0,  n_req=10**3, seed=None, **kwargs):

        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.egress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'egress_node']
        self.rate = rate
        self.n_req = n_req
        random.seed(seed)


    @staticmethod
    def select_random_sfc():

        services = [[1, 2],  # [nat - fw]
                    [4, 5],  # [wanopt - lb]
                    [1, 2, 3],  # [nat - fw - ids]
                    [2, 3, 5],  # [fw - ids - lb]
                    [1, 5, 4],  # [nat - lb - wanopt]
                    [5, 2, 1],  # [lb - fw - nat]
                    [2, 3, 5, 6],  # [fw - ids - lb - encrypt]
                    [3, 2, 5, 4],  # [ids - fw - lb - wanopt]
                    [5, 4, 6, 2, 3],  # [lb - wanopt - encrypt - fw - ids]
                    [5, 4, 1, 2, 6, 7]  # [lb - wanopt - nat - fw - encrypt - decrypt]
                    ]

        return random.choice(services)


    def __iter__(self):
        req_counter = 0
        t_event = 0.0
        while req_counter < self.n_req:
            t_event += (random.expovariate(self.rate))
            ingress_node = random.choice(self.ingress_nodes)
            egress_node = random.choice(self.egress_nodes)
            sfc = StationaryWorkloadRandomSfc.select_random_sfc()
            log = (req_counter < self.n_req)
            event = {'ingress_node': ingress_node, 'egress_node': egress_node, 'sfc': sfc, 'log': log}
            yield (t_event, event)
            req_counter += 1
        raise StopIteration()


class StationaryWorkloadVarLenSfc:
    """
    This function generates events on the fly, i.e. instead of creating an
    event schedule to be kept in memory, returns an iterator that generates
    events when needed.

    This is useful for running large schedules of events where RAM is limited
    as its memory impact is considerably lower

    All requests are mapped to receivers uniformly unless a positive *beta*
    parameter is specified


    """

    def __init__(self, topology, rate=1.0,  n_req=10 ** 3, seed=None, **kwargs):

        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.egress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'egress_node']
        self.rate = rate
        self.n_req = n_req
        random.seed(seed)


    @staticmethod
    def var_seq_len_sfc():
        sfc = []
        vnfs = [1, 2, 3, 4, 5, 6, 7]  # vnfs available for service function chaining
        n = random.randint(1, 8)  # n_vnfs + 1
        for i in range(1, n + 1):
            vnf = random.choice(vnfs)
            if vnf not in sfc:
                sfc.append(vnf)
        return sfc

    def __iter__(self):
        req_counter = 0
        t_event = 0.0
        while req_counter < self.n_req:
            t_event += (random.expovariate(self.rate))
            ingress_node = random.choice(self.ingress_nodes)
            egress_node = random.choice(self.egress_nodes)
            sfc = StationaryWorkloadVarLenSfc.var_seq_len_sfc()
            log = (req_counter < self.n_req)
            event = {'ingress_node': ingress_node, 'egress_node': egress_node, 'sfc': sfc, 'log': log}
            yield (t_event, event)
            req_counter += 1
        raise StopIteration()




topo = topology_tatanld()

print(len(topo.nodes()))
workload = StationaryWorkloadVarLenSfc(topo)
for i in workload:
    print(i)






