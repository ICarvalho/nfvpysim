import random
import networkx as nx
from tools.stats import TruncatedZipfDist


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

    def __init__(self, topology, n_sfcs, alpha,  beta=0, rate=1.0, n_req=10**5, seed=None, **kwargs):

        if beta < 0:
            raise ValueError('beta must be positive')
        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.zipf = TruncatedZipfDist(alpha, n_sfcs)
        self.n_sfcs = n_sfcs
        self.alpha = alpha
        self.rate = rate
        self.n_req = n_req
        random.seed(seed)
        if beta != 0:
            degree = nx.degree(topology)
            self.ingress_nodes = sorted(self.ingress_nodes, key=lambda x: degree[iter(topology.edge[x]).next()], reverse=True)
            self.ingress_nodes_dist = TruncatedZipfDist(beta, len(self.ingress_nodes))

    def __iter__(self):
        req_counter = 0
        t_event = 0.0
        while req_counter < self.n_req:
            t_event += (random.expovariate(self.rate))
            if self.beta == 0:
                ingress_node = random.choice(self.ingress_nodes)
            else:
                ingress_node = self.ingress_nodes[self.ingress_nodes_dist.rv() - 1]
            sfc = int(self.zipf.rv())
            log = (req_counter <= self.n_req)
            event = {'requester': ingress_node, 'SFC': sfc, 'log': log}
            yield (t_event, event)
            req_counter += 1
        raise StopIteration()


