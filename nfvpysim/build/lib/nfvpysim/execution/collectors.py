from nfvpysim.util import Tree
from nfvpysim.registry import register_data_collector
from nfvpysim.tools.stats import cdf
import collections

__all__ = [
    'DataCollector',
    'CollectorProxy',
    'AcceptanceRatioCollector',
    'LatencyCollector',
    'LinkLoadCollector',
    'PathStretchCollector'
]


class DataCollector:

    def __init__(self, view, **params):
        self.view = view

    def start_session(self, timestamp, sfc_id, ingress_node, egress_node, sfc, delay):
        pass

    def request_vnf_hop(self, u, v, main_path=True):
        pass

    def vnf_proc_payload(self, u, v, main_path=True):
        pass

    def sfc_hit(self, sfc_id):
        pass

    def get_sess_latency(self):
        pass

    def vnf_proc_delay(self, vnf):
        pass

    def end_session(self, success=True):
        pass

    def results(self):
        pass


class CollectorProxy(DataCollector):
    EVENTS = ('start_session', 'request_vnf_hop', 'vnf_proc_payload', 'sfc_hit', 'vnf_proc_delay', 'get_sess_latency',
              'end_session', 'results')

    def __init__(self, view, collectors, **params):

        super().__init__(view, **params)
        self.view = view
        self.collectors = {e: [c for c in collectors if e in type(c).__dict__]
                           for e in self.EVENTS}

    def start_session(self, timestamp, sfc_id, ingress_node, egress_node, sfc, delay):
        for c in self.collectors['start_session']:
            c.start_session(timestamp, sfc_id, ingress_node, egress_node, sfc, delay)

    def request_vnf_hop(self, u, v, main_path=True):
        for c in self.collectors['request_vnf_hop']:
            c.request_vnf_hop(u, v, main_path)

    def vnf_proc_payload(self, u, v, main_path=True):
        for c in self.collectors['vnf_proc_payload']:
            c.vnf_proc_payload(u, v, main_path)

    def sfc_hit(self, sfc_id):
        for c in self.collectors['sfc_hit']:
            c.sfc_hit(sfc_id)

    def vnf_proc_delay(self, vnf):
        for c in self.collectors['vnf_proc_delay']:
            c.vnf_proc_delay(vnf)

    def get_sess_latency(self):
        for c in self.collectors['get_sess_latency']:
            c.get_sess_latency()

    def end_session(self, success=True):
        for c in self.collectors['end_session']:
            c.end_session(success)

    def results(self):
        return Tree(**{c.name: c.results() for c in self.collectors['results']})


@register_data_collector('LINK_LOAD')
class LinkLoadCollector(DataCollector):
    """Data collector measuring the link load
    """

    def __init__(self, view, req_size=1000, **params):
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
        super().__init__(view, **params)
        self.view = view
        self.req_count = collections.defaultdict(int)
        if req_size <= 0:
            raise ValueError('req_size  must be positive')
        self.req_size = req_size

        self.t_start = -1
        self.t_end = 1

    def start_session(self, timestamp, sfc_id, ingress_node, egress_node, sfc, delay):
        if self.t_start < 0:
            self.t_start = timestamp
        self.t_end = timestamp

    def request_vnf_hop(self, u, v, path=True):
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
        return Tree({'MEAN_INTERNAL': mean_load_int,
                     'MEAN_EXTERNAL': mean_load_ext,
                     'PER_LINK_INTERNAL': link_loads_int,
                     'PER_LINK_EXTERNAL': link_loads_ext})


@register_data_collector('LATENCY')
class LatencyCollector(DataCollector):
    """Data collector measuring latency, i.e. the delay taken to delivery a
    content.
    """

    def __init__(self, view, cdf=True, **params):
        """Constructor
        Parameters
        ----------
        view : NetworkView
            The network view instance
        cdf : bool, optional
            If *True*, also collects a cdf of the latency
        """
        super().__init__(view, **params)
        self.cdf = cdf
        self.view = view
        self.sess_latency = 0.0
        self.req_latency = 0.0
        self.sess_count = 0
        self.latency = 0.0
        self.vnf_proc_time = 0.0
        self.dict_vnfs_cpu_req_proc_delay = {0: 15,  # nat
                                             1: 25,  # fw
                                             2: 25,  # ids
                                             3: 20,  # wanopt
                                             4: 20,  # lb
                                             5: 25,  # encrypt
                                             6: 25,  # decrypts
                                             7: 30  # dpi
                                             }

        if cdf:
            self.latency_data = collections.deque()

    def start_session(self, timestamp, sfc_id, ingress_node, egress_node, sfc, delay):
        self.sess_count += 1
        self.sess_latency = 0.0
        self.vnf_proc_time = 0.0

    """
    @staticmethod
    def get_vnf_proc_delay(lower, upper):
        delay = random.uniform(lower, upper)
        return round(delay, 2)
    """

    def request_vnf_hop(self, u, v, path=True):
        if path:
            self.sess_latency += self.view.link_delay(u, v)

    def vnf_proc_delay(self, vnf):
        if vnf in self.dict_vnfs_cpu_req_proc_delay.keys():
            self.sess_latency += self.dict_vnfs_cpu_req_proc_delay[vnf]

    def get_sess_latency(self):
        return self.sess_latency

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


@register_data_collector('ACCEPTANCE_RATIO')
class AcceptanceRatioCollector(DataCollector):
    """
    Data Collector measuring the Acceptance Ratio of requested VNFs

    """

    def __init__(self, view, per_sfc=True, **params):

        super().__init__(view, **params)
        self.per_sfc = per_sfc
        self.view = view
        self.sess_count = 0
        self.sfc_hits = 0
        self.curr_path = None

        if per_sfc:
            self.per_sfc_hit = collections.defaultdict(int)

    def start_session(self, timestamp, sfc_id, ingress_node, egress_node, sfc, delay):
        self.sess_count += 1
        self.curr_path = self.view.shortest_path(ingress_node, egress_node)

    def sfc_hit(self, sfc_id):
        self.sfc_hits += 1
        if self.per_sfc_hit:
            self.self.per_sfc_hit[sfc_id] += 1

    def results(self):
        n_sess = self.sess_count
        sfc_hit_ratio = self.sfc_hits / n_sess
        results = Tree(**{'MEAN': sfc_hit_ratio})
        if self.per_sfc:
            for sfc in self.per_sfc_hit:
                self.per_sfc_hit[sfc] /= n_sess
            results['PER_SFC_HIT_RATIO'] = self.per_sfc_hit

        return results


@register_data_collector("PATH_STRETCH")
class PathStretchCollector(DataCollector):
    """Collector measuring the path stretch, i.e. the ratio between the actual
    path length and the shortest path length.
    """

    def __init__(self, view, cdf=False, **params):
        """Constructor
        Parameters
        ----------
        view : NetworkView
            The network view instance
        cdf : bool, optional
            If *True*, also collects a cdf of the path stretch
        """
        super().__init__(view, **params)
        self.view = view
        self.sp = None
        self.ingress_node = None
        self.egress_node = None
        self.sp_len = 0
        self.cdf = cdf
        self.req_path_len = collections.defaultdict(int)
        self.sess_count = 0
        self.mean_stretch = 0.0
        if self.cdf:
            self.req_stretch_data = collections.deque()
            self.stretch_data = collections.deque()

    def start_session(self, timestamp, sfc_id, ingress_node, egress_node, sfc, delay):
        self.req_path_len = 0
        self.sess_count += 1
        self.ingress_node = ingress_node
        self.egress_node = egress_node

    def request_vnf_hop(self, u, v, main_path=True):
        self.req_path_len += 1

    def end_session(self, success=True):
        if not success:
            return
        req_sp_len = len(self.view.shortest_path(self.ingress_node, self.egress_node))
        req_stretch = self.req_path_len / req_sp_len
        self.mean_stretch += req_stretch

    def results(self):
        results = Tree(
            {
                "MEAN": self.mean_stretch / self.sess_count
            }
        )

        return results
