import random
import networkx as nx
from tools.stats import TruncatedZipfDist
from topologies.topology import topology_geant


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

    def __init__(self, topology, n_sfcs, alpha,  beta=0, rate=1.0, n_req=10**3, seed=None, **kwargs):

        if beta < 0:
            raise ValueError('beta must be positive')
        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.zipf = TruncatedZipfDist(alpha, n_sfcs)
        self.n_sfcs = n_sfcs
        self.alpha = alpha
        self.beta = beta
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




class TraceDrivenWorkload:
    """Parse requests from a generic request trace.
    This workload requires two text files:
     * a requests file, where each line corresponds to a string identifying
       the content requested
     * a contents file, which lists all unique content identifiers appearing
       in the requests file.
    Since the trace do not provide timestamps, requests are scheduled according
    to a Poisson process of rate *rate*. All requests are mapped to receivers
    uniformly unless a positive *beta* parameter is specified.
    If a *beta* parameter is specified, then receivers issue requests at
    different rates. The algorithm used to determine the requests rates for
    each receiver is the following:
     * All receiver are sorted in decreasing order of degree of the PoP they
       are attached to. This assumes that all receivers have degree = 1 and are
       attached to a node with degree > 1
     * Rates are then assigned following a Zipf distribution of coefficient
       beta where nodes with higher-degree PoPs have a higher request rate
    Parameters
    ----------
    topology : fnss.Topology
        The topology to which the workload refers
    reqs_file : str
        The path to the requests file
    contents_file : str
        The path to the contents file
    n_contents : int
        The number of content object (i.e. the number of lines of contents_file)
    n_warmup : int
        The number of warmup requests (i.e. requests executed to fill cache but
        not logged)
    n_measured : int
        The number of logged requests after the warmup
    rate : float, optional
        The network-wide mean rate of requests per second
    beta : float, optional
        Spatial skewness of requests rates
    Returns
    -------
    events : iterator
        Iterator of events. Each event is a 2-tuple where the first element is
        the timestamp at which the event occurs and the second element is a
        dictionary of event attributes.
    """

    def __init__(self, topology, reqs_file, contents_file, n_contents,
                 n_warmup, n_measured, rate=1.0, beta=0, **kwargs):
        """Constructor"""
        if beta < 0:
            raise ValueError('beta must be positive')
        # Set high buffering to avoid one-line reads
        self.buffering = 64 * 1024 * 1024
        self.n_contents = n_contents
        self.n_warmup = n_warmup
        self.n_measured = n_measured
        self.reqs_file = reqs_file
        self.rate = rate
        self.receivers = [v for v in topology.nodes()
                          if topology.node[v]['stack'][0] == 'receiver']
        self.contents = []
        with open(contents_file, 'r', buffering=self.buffering) as f:
            for content in f:
                self.contents.append(content)
        self.beta = beta
        if beta != 0:
            degree = nx.degree(topology)
            self.receivers = sorted(self.receivers, key=lambda x:
                                    degree[iter(topology.adj[x]).next()],
                                    reverse=True)
            self.receiver_dist = TruncatedZipfDist(beta, len(self.receivers))

    def __iter__(self):
        req_counter = 0
        t_event = 0.0
        with open(self.reqs_file, 'r', buffering=self.buffering) as f:
            for content in f:
                t_event += (random.expovariate(self.rate))
                if self.beta == 0:
                    receiver = random.choice(self.receivers)
                else:
                    receiver = self.receivers[self.receiver_dist.rv() - 1]
                log = (req_counter >= self.n_warmup)
                event = {'receiver': receiver, 'content': content, 'log': log}
                yield (t_event, event)
                req_counter += 1
                if(req_counter >= self.n_warmup + self.n_measured):
                    return
            raise ValueError("Trace did not contain enough requests")




#topology, n_sfcs, alpha,  beta=0, rate=1.0, n_req=10**5, seed=None, **kwargs
topo = topology_geant()
workload = StationaryWorkload(topo, 10, 1)
for i in workload:
    print(i)