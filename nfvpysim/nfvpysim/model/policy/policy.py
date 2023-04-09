from abc import abstractmethod, ABC
from collections import defaultdict

import networkx as nx
from nfvpysim.registry import register_policy

# from nfvpysim.util import path_links

__all__ = [
    'Policy',
    'Bcsp',
    'TapAlgo',
    'FirstOrder',
    'Markov',
    'Baseline',
    'Hod',
    'HodOff',
    'HodDeg',
    'HodClose',
    'HodPage',
    'HodEigen',
    'FirstFit'
]


class Policy:
    def __init__(self, view, controller, **kwargs):
        self.view = view
        self.controller = controller

    @abstractmethod
    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        raise NotImplementedError('The selected policy must implement a process event method')


@register_policy('BCSP')
class Bcsp(Policy):
    def __init__(self, view, controller, **kwargs):
        super(Bcsp, self).__init__(view, controller)
        topology = view.topology()
        self.betw = nx.betweenness_centrality(topology)
        self.nfv_nodes = [v for v in topology if topology.node[v]["stack"][0] == "nfv_node"]

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def find_highest_betw_node(self, path):
        max_betw = -1
        highest_betw_node = None
        for node in path:
            if self.betw[node] > max_betw and node in self.nfv_nodes:
                max_betw = self.betw[node]
                highest_betw_node = node
        return highest_betw_node

    def place_sfc_on_highest_betw_node(self, path, sfc):
        highest_betw_node = self.find_highest_betw_node(path)
        for node in path:
            if node == highest_betw_node:
                for vnf in sfc:
                    self.controller.put_vnf(node, vnf)
        return None

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        path = self.view.shortest_path(ingress_node, egress_node)
        self.place_sfc_on_highest_betw_node(path, sfc)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = Bcsp.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('TAP_ALGO')
class TapAlgo(Policy):
    def __init__(self, view, controller, **kwargs):
        super(TapAlgo, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def find_path(self, ingress_node, egress_node, sfc, delay):
        topology = self.view.topology()
        paths = self.controller.get_all_paths(topology, ingress_node, egress_node)  # list of (list) paths
        target_path = self.controller.sort_paths_min_cpu_use(paths)
        sum_cpu_sfc = TapAlgo.sum_vnfs_cpu(sfc)
        dict_node_cpu = {}
        if self.controller.nodes_rem_cpu(target_path) > sum_cpu_sfc and self.view.delay_path(target_path) < delay:
            nfv_nodes = self.controller.nfv_nodes_path(target_path)
            for node in nfv_nodes:
                dict_node_cpu[node] = self.controller.sum_vnfs_cpu_on_node(node)
            node_max_cpu = min(dict_node_cpu.keys())
            node_max_cpu_avail = dict_node_cpu[node_max_cpu]
            for node in target_path:
                if node == node_max_cpu:
                    if sum_cpu_sfc <= node_max_cpu_avail:
                        self.controller.put_sfc(node, sfc)
                        break

                else:
                    continue

        return target_path

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = TapAlgo.sum_vnfs_cpu(sfc)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        path = self.find_path(ingress_node, egress_node, sfc, delay)
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('FIRST_FIT')
class FirstFit(Policy, ABC):
    def __init__(self, view, controller, **kwargs):
        super(FirstFit, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def first_fit_search(self, path, sfc):
        sum_cpu_nodes = {}
        sum_vnfs_sfc = FirstFit.sum_vnfs_cpu(sfc)
        for node in path:
            sum_cpu_nodes[node] = self.controller.sum_vnfs_cpu_on_node(node)
            if sum_cpu_nodes[node] <= sum_vnfs_sfc:
                self.controller.put_sfc(node, sfc)
                break
        return

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = FirstFit.sum_vnfs_cpu(sfc)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        path = self.view.shortest_path(ingress_node, egress_node)

        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('MARKOV')
class Markov(Policy):
    def __init__(self, view, controller, **kwargs):
        super(Markov, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = FirstOrder.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('FIRST_ORDER')
class FirstOrder(Policy):
    def __init__(self, view, controller, **kwargs):
        super(FirstOrder, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = FirstOrder.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('BASELINE')
class Baseline(Policy):

    def __init__(self, view, controller, **kwargs):
        super(Baseline, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = FirstOrder.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        delay_sfc[sfc_id] = sum_cpu_sfc
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
                delay_sfc[sfc_id] += sum_cpu_sfc
            # print(delay_sfc[sfc_id])
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                print(delay_sfc)
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('HOD_VNF')
class Hod(Policy):

    def __init__(self, view, controller):
        super(Hod, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 20,  # nat
                    1: 25,  # fw
                    2: 30,  # ids
                    3: 35,  # wanopt
                    4: 40,  # lb
                    5: 45,  # encrypt
                    6: 50,  # decrypts
                    7: 55  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = {}  # dict to store the delay taken to run the sfc over the path
        missed_vnfs = []
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = Hod.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        delay_sfc[sfc_id] = 0.0
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v) and v != egress_node:
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
                        elif vnf_status[vnf] == 1:
                            continue
                    else:
                        missed_vnfs.append(vnf)

            if len(missed_vnfs) != 0:
                sum_cpu_missed_vnfs = Hod.sum_vnfs_cpu(missed_vnfs)
                nfv_node_min_cpu_all = self.controller.find_nfv_node_with_min_cpu_alloc(ingress_node, egress_node)
                closest_nfv_node = self.controller.get_closest_nfv_node(path)
                # sum_cpu_vnfs_on_node = self.controller.sum_vnfs_cpu_on_node(closest_nfv_node)
                if v == closest_nfv_node:  # and v == nfv_node_min_cpu_all:
                    for missed_vnf in missed_vnfs:
                        vnf_status[missed_vnf] = 1
                        self.controller.put_vnf(v, missed_vnf)
                        # self.controller.vnf_proc(missed_vnf)
                        self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break
        self.controller.end_session()


@register_policy('HOD_VNF_OFF')
class HodOff(Policy):

    def __init__(self, view, controller):
        super(HodOff, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = {}  # dict to store the delay taken to run the sfc over the path
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = Hod.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        delay_sfc[sfc_id] = 0
        for hop in range(1, len(path)):
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('HOD_DEG')
class HodDeg(Policy):

    def __init__(self, view, controller, **kwargs):
        super(HodDeg, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        missed_vnfs = []
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = HodDeg.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v) and v != egress_node:
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
                        elif vnf_status[vnf] == 1:
                            continue
                    else:
                        missed_vnfs.append(vnf)

            if len(missed_vnfs) != 0:
                # sum_cpu_missed_vnfs = Hod.sum_vnfs_cpu(missed_vnfs)
                # nfv_node_min_cpu_all = self.controller.find_nfv_node_with_min_cpu_alloc(ingress_node, egress_node)
                closest_nfv_node = self.controller.get_closest_nfv_node(path)
                # sum_cpu_vnfs_on_node = self.controller.sum_vnfs_cpu_on_node(closest_nfv_node)
                if v == closest_nfv_node:  # and v == nfv_node_min_cpu_all:
                    for missed_vnf in missed_vnfs:
                        vnf_status[missed_vnf] = 1
                        self.controller.put_vnf(v, missed_vnf)
                        # self.controller.vnf_proc(missed_vnf)
                        self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('HOD_CLOSE')
class HodClose(Policy):

    def __init__(self, view, controller, **kwargs):
        super(HodClose, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        missed_vnfs = []
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = HodClose.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v) and v != egress_node:
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
                        elif vnf_status[vnf] == 1:
                            continue
                    else:
                        missed_vnfs.append(vnf)

            if len(missed_vnfs) != 0:
                sum_cpu_missed_vnfs = Hod.sum_vnfs_cpu(missed_vnfs)
                nfv_node_min_cpu_all = self.controller.find_nfv_node_with_min_cpu_alloc(ingress_node, egress_node)
                closest_nfv_node = self.controller.get_closest_nfv_node(path)
                # sum_cpu_vnfs_on_node = self.controller.sum_vnfs_cpu_on_node(closest_nfv_node)
                if v == closest_nfv_node:  # and v == nfv_node_min_cpu_all:
                    for missed_vnf in missed_vnfs:
                        vnf_status[missed_vnf] = 1
                        self.controller.put_vnf(v, missed_vnf)
                        # self.controller.vnf_proc(missed_vnf)
                        self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('HOD_PAGE')
class HodPage(Policy):

    def __init__(self, view, controller, **kwargs):
        super(HodPage, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        missed_vnfs = []
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = HodPage.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v) and v != egress_node:
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
                        elif vnf_status[vnf] == 1:
                            continue
                    else:
                        missed_vnfs.append(vnf)

            if len(missed_vnfs) != 0:
                sum_cpu_missed_vnfs = Hod.sum_vnfs_cpu(missed_vnfs)
                nfv_node_min_cpu_all = self.controller.find_nfv_node_with_min_cpu_alloc(ingress_node, egress_node)
                closest_nfv_node = self.controller.get_closest_nfv_node(path)
                # sum_cpu_vnfs_on_node = self.controller.sum_vnfs_cpu_on_node(closest_nfv_node)
                if v == closest_nfv_node:  # and v == nfv_node_min_cpu_all:
                    for missed_vnf in missed_vnfs:
                        vnf_status[missed_vnf] = 1
                        self.controller.put_vnf(v, missed_vnf)
                        # self.controller.vnf_proc(missed_vnf)
                        self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


@register_policy('HOD_EIGEN')
class HodEigen(Policy):

    def __init__(self, view, controller, **kwargs):
        super(HodEigen, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {0: 15,  # nat
                    1: 25,  # fw
                    2: 25,  # ids
                    3: 20,  # wanopt
                    4: 20,  # lb
                    5: 25,  # encrypt
                    6: 25,  # decrypts
                    7: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int)  # dict to store the delay taken to run the sfc over the path
        missed_vnfs = []
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = HodEigen.sum_vnfs_cpu(sfc)  # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v) and v != egress_node:
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
                        elif vnf_status[vnf] == 1:
                            continue
                    else:
                        missed_vnfs.append(vnf)

            if len(missed_vnfs) != 0:
                sum_cpu_missed_vnfs = Hod.sum_vnfs_cpu(missed_vnfs)
                nfv_node_min_cpu_all = self.controller.find_nfv_node_with_min_cpu_alloc(ingress_node, egress_node)
                closest_nfv_node = self.controller.get_closest_nfv_node(path)
                # sum_cpu_vnfs_on_node = self.controller.sum_vnfs_cpu_on_node(closest_nfv_node)
                if v == closest_nfv_node:  # and v == nfv_node_min_cpu_all:
                    for missed_vnf in missed_vnfs:
                        vnf_status[missed_vnf] = 1
                        self.controller.put_vnf(v, missed_vnf)
                        # self.controller.vnf_proc(missed_vnf)
                        self.controller.proc_vnf_payload(u, v)
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()


"""
        for hop in range(1, len(path)):
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            # self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
            if all(value == 1 for value in vnf_status.values()) and v == egress_node:
                self.controller.sfc_hit(sfc_id)

        self.controller.end_session()


"""

"""
         for hop in range(1, len(path)):
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            if self.view.is_nfv_node(v) and v != egress_node:
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            #self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
                    else:
                        missed_vnfs.append(vnf)

            if len(missed_vnfs) != 0:
                sum_cpu_missed_vnfs = GreedyWithOnlinePlacementPolicy.sum_vnfs_cpu(missed_vnfs)
                nfv_node_min_cpu_all = self.controller.find_nfv_node_with_min_cpu_alloc(ingress_node, egress_node)
                closest_nfv_node = self.controller.get_closest_nfv_node(path)
                # sum_cpu_vnfs_on_node = self.controller.sum_vnfs_cpu_on_node(closest_nfv_node)
                if v == closest_nfv_node: # and v == nfv_node_min_cpu_all:
                    for missed_vnf in missed_vnfs:
                        vnf_status[missed_vnf] = 1
                        self.controller.put_vnf(v, missed_vnf)
                        #self.controller.vnf_proc(missed_vnf)
                        self.controller.proc_vnf_payload(u, v)
            if all(value == 1 for value in vnf_status.values()) and v == egress_node:
                self.controller.sfc_hit(sfc_id)

        self.controller.end_session()




"""
