from nfvpysim.util import Tree
from nfvpysim.tools.stats import cdf
import collections




class DataCollector:

    def __init__(self, view, **params):

        self.view = view


    def start_session(self, timestamp, ingress_node, sfc):

        pass


    def request_hop(self, u, v, path):

        pass

    def enabled_path(self, path):

        pass


    def sfc_acc(self, sfc):

        pass



    def end_session(self, success=True):

        pass


    def results(self):

        pass



class CollectorProxy(DataCollector):


    EVENTS = ('start_session', 'sfc_acc' 'end_session', 'request_hop', 'results')

    def __init__(self, view, collectors):

        self.view = view
        self.collectors =  {e: [c for c in collectors if e in type(c).__dict__]
                             for e in self.EVENTS}


    def start_session(self, timestamp, ingress_node, sfc):
        for c in self.collectors['start_session']:
            c.start_session(timestamp, ingress_node, sfc)



    def request_hop(self, u, v, path=True):
        for c in self.collectors['request_hop']:
            c.request_hop(u, v, path)


    def sfc_acc(self, sfc ):
        for c in self.collectors['sfc_acc']:
            c.sfc_acc(sfc)




    def end_session(self, success=True):
        for c in self.collectors['end_session']:
            c.end_session(success)


    def results(self):
        return Tree(**{c.name: c.results() for c in self.collectors['results']})


class LinkLoadCollector(DataCollector):
    """Data collector measuring the link load
    """

    def __init__(self, view, req_size=1500):
        """Constructor
        Parameters
        ----------
        view : NetworkView
            The network view instance
        req_size : int
            Average size (in bytes) of a request
        content_size : int
            Average size (in byte) of a content
        """
        self.view = view
        self.req_count = collections.defaultdict(int)
        if req_size <= 0:
            raise ValueError('req_size  must be positive')
        self.req_size = req_size

        self.t_start = -1
        self.t_end = 1


    def start_session(self, timestamp, ingress_node, egress_node,  sfc):
        if self.t_start < 0:
            self.t_start = timestamp
        self.t_end = timestamp

    def request_hop(self, u, v, path=True):
        self.req_count[(u, v)] += 1



    def results(self):
        duration = self.t_end - self.t_start
        used_links = set(self.req_count.keys())
        link_loads = {link: (self.req_size * self.req_count[link]) / duration
                      for link in used_links}
        link_loads_int = {link: load
                          for link, load in link_loads.items()
                          if self.view.link_type(*link) == 'internal'}
        link_loads_ext = {link: load
                          for link, load in link_loads.items()
                          if self.view.link_type(*link) == 'external'}
        mean_load_int = sum(link_loads_int.values()) / len(link_loads_int) \
            if len(link_loads_int) > 0 else 0
        mean_load_ext = sum(link_loads_ext.values()) / len(link_loads_ext) \
            if len(link_loads_ext) > 0 else 0
        return Tree({'MEAN_INTERNAL':     mean_load_int,
                     'MEAN_EXTERNAL':     mean_load_ext,
                     'PER_LINK_INTERNAL': link_loads_int,
                     'PER_LINK_EXTERNAL': link_loads_ext})




class LatencyCollector(DataCollector):
    """Data collector measuring latency, i.e. the delay taken to delivery a
    content.
    """

    def __init__(self, view, cdf=False):
        """Constructor
        Parameters
        ----------
        view : NetworkView
            The network view instance
        cdf : bool, optional
            If *True*, also collects a cdf of the latency
        """
        self.cdf = cdf
        self.view = view
        self.req_latency = 0.0
        self.sess_count = 0
        self.latency = 0.0
        if cdf:
            self.latency_data = collections.deque()


    def start_session(self, timestamp, ingress_node, egress_node, sfc):
        self.sess_count += 1
        self.sess_latency = 0.0


    def request_hop(self, u, v, path=True):
        if path:
            self.sess_latency += self.view.link_delay(u, v)


    def end_session(self, success=True):
        if not success:
            return
        if self.cdf:
            self.latency_data.append(self.sess_latency)
        self.latency += self.sess_latency


    def results(self):
        results = Tree({'MEAN': self.latency / self.sess_count})
        if self.cdf:
            results['CDF'] = cdf(self.latency_data)
        return results



class AcceptanceRatio(DataCollector):
    """
    Data Collector measuring the Acceptance Ratio of requested VNFs

    """

    def __init__(self, view, per_sfc=True ):

        self.view = view
        self.sess_count = 0
        self.acc_sfc = 0

        if per_sfc:
            self.per_sfc_ratio = collections.defaultdict(int)

        def start_session(self, timestamp, ingress_node, egress_node, sfc):
            self.sess_count += 1
            self.curr_path = self.view.shortest_path(ingress_node, egress_node)


        def sfc_acc(self, sfc):
            self.acc_sfc += 1
            if self.per_sfc_ratio:
                self.per_sfc_ratio[sfc] += 1

        def results(self):
            n_sess = self.acc_sfc
            sfc_acc_ratio = self.acc_sfc / n_sess
            results = Tree(**{'MEAN': sfc_acc_ratio})

            return results


