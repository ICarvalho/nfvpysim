from nfvpysim.util import Tree
from nfvpysim.registry import register_data_collector
from nfvpysim.tools.stats import cdf
import collections



__all__ = [
    'DataCollector',
    'CollectorProxy',
    'AcceptanceRatioCollector',
    'LinkLoadCollector',
    'LatencyCollector'
           ]




class DataCollector:

    def __init__(self, view, **params):

        self.view = view


    def start_session(self, timestamp, ingress_node, egress_node, sfc):
        pass

    def request_vnf_hop(self, u, v, main_path=True):
        pass

    def vnf_proc_payload(self, u, v, main_path=True):
        pass


    def sfc_hit(self, sfc):
        pass

    def vnf_proc_delay(self, vnf):
        pass

    def end_session(self, success=True):
        pass

    def results(self):
        pass



class CollectorProxy(DataCollector):


    EVENTS = ('start_session', 'request_vnf_hop', 'vnf_proc_payload', 'sfc_hit', 'vnf_proc_delay', 'end_session',  'results')

    def __init__(self, view, collectors, **params):

        super().__init__(view, **params)
        self.view = view
        self.collectors = {e: [c for c in collectors if e in type(c).__dict__]
                             for e in self.EVENTS}


    def start_session(self, timestamp, ingress_node, egress_node, sfc):
        for c in self.collectors['start_session']:
            c.start_session(timestamp, ingress_node, egress_node, sfc)



    def request_vnf_hop(self, u, v, main_path=True):
        for c in self.collectors['request_vnf_hop']:
            c.request_vnf_hop(u, v, main_path)

    def vnf_proc_payload(self, u, v, main_path=True):
        for c in self.collectors['vnf_proc_payload']:
            c.vnf_proc_payload(u, v, main_path)


    def sfc_hit(self, sfc):
        for c in self.collectors['sfc_hit']:
            c.sfc_hit(sfc)


    def vnf_proc_delay(self, vnf):
        for c in self.collectors['vnf_proc_delay']:
            c.vnf_proc_delay(vnf)


    def end_session(self, success=True):
        for c in self.collectors['end_session']:
            c.end_session(success)


    def results(self):
        return Tree(**{c.name: c.results() for c in self.collectors['results']})


@register_data_collector('LINK_LOAD')
class LinkLoadCollector(DataCollector):
    """Data collector measuring the link load
    """

    def __init__(self, view, req_vnf_size=150, vnf_payload=1500, **params):
        """Constructor
        Parameters
        ----------
        view : NetworkView
            The network view instance
        req_vnf_size: int
            average size of a vnf request in bytes

        vnf_payload : int
            Average payload of a given vnf in bytes
        """
        super().__init__(view, **params)
        self.view = view
        self.req_vnf_count = collections.defaultdict(int)
        self.vnf_proc_payload_count = collections.defaultdict(int)
        if req_vnf_size <= 0:
            raise ValueError('req_size  must be positive')
        self.req_vnf_size = req_vnf_size
        self.vnf_payload = vnf_payload

        self.t_start = -1
        self.t_end = 1


    def start_session(self, timestamp, ingress_node, egress_node, sfc):
        if self.t_start < 0:
            self.t_start = timestamp
        self.t_end = timestamp

    def request_vnf_hop(self, u, v, path=True):
        self.req_vnf_count[(u, v)] += 1

    def vnf_proc_payload(self, u, v, path=True):
        self.vnf_proc_payload_count[(u, v)] += 1


    def results(self):
        duration = self.t_end - self.t_start
        used_links = set(self.req_vnf_count.keys()).union(set(self.vnf_proc_payload_count.keys()))
        link_loads = {link: (self.req_vnf_size * self.vnf_proc_payload_count[link] +
                             self.vnf_payload * self.vnf_proc_payload_count[link]) / duration
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



@register_data_collector('LATENCY')

class LatencyCollector(DataCollector):
    """Data collector measuring latency, i.e. the delay taken to delivery a
    content.
    """

    def __init__(self, view, cdf=False, **params):
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
        self.dict_vnfs_cpu_req_proc_delay = {1: 15,  # nat
                                             2: 25,  # fw
                                             3: 25,  # ids
                                             4: 20,  # wanopt
                                             5: 20,  # lb
                                             6: 25,  # encrypt
                                             7: 25,  # decrypt
                                             8: 30,  # dpi
                                             }

        if cdf:
            self.latency_data = collections.deque()


    def start_session(self, timestamp, ingress_node, egress_node, sfc):
        self.sess_count += 1
        self.sess_latency = 0.0

    def request_vnf_hop(self, u, v, path=True):
        if path:
            self.sess_latency += self.view.link_delay(u, v)

    def vnf_proc_delay(self, vnf):
        if vnf in self.dict_vnfs_cpu_req_proc_delay.keys():
            self.sess_latency += self.dict_vnfs_cpu_req_proc_delay[vnf]


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
        self.view = view
        self.sess_count = 0
        self.sfc_hit = 0

        if per_sfc:
            self.per_sfc_ratio = collections.defaultdict(int)

    def start_session(self, timestamp, ingress_node, egress_node, sfc):
        self.sess_count += 1
        self.curr_path = self.view.shortest_path(ingress_node, egress_node)


    def sfc_hit(self, sfc):
        self.sfc_hit += 1
        if self.per_sfc_ratio:
            self.per_sfc_ratio[sfc] += 1

    def results(self):
        n_sess = self.sfc_hit
        sfc_hit_ratio = self.sfc_hit / n_sess
        results = Tree(**{'MEAN': sfc_hit_ratio})

        return results


