from abc import abstractmethod, ABC
from collections import defaultdict
from nfvpysim.registry import register_policy

# from nfvpysim.util import path_links

__all__ = [
    'Policy',
    'TapAlgo',
    'FirstOrder',
    'Greedy',
    'Hod'
]


class Policy:

    def __init__(self, view, controller, **kwargs):
        self.view = view
        self.controller = controller

    @abstractmethod
    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        raise NotImplementedError('The selected policy must implement a process event method')



@register_policy('TAP_ALGO')
class TapAlgo(Policy):
    def __init__(self, view, controller, **kwargs):
        super(TapAlgo, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {1: 10,  # nat
                    2: 25,  # fw
                    3: 25,  # ids
                    4: 20,  # wanopt
                    5: 20,  # lb
                    6: 25,  # encrypt
                    7: 25,  # decrypts
                    8: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        topology = self.view.topology()
        paths = self.controller.get_all_paths(topology, ingress_node, egress_node)
        sum_cpu = TapAlgo.sum_vnfs_cpu(sfc)
        dict_node_cpu = {}
        for path in paths:
            if self.controller.path_capacity_rem_cpu(path) > sum_cpu and self.view.delay_path(path) < delay:
                nfv_nodes =self.controller.nfv_nodes_path(topology, path)
                for node in nfv_nodes:
                    dict_node_cpu[node] = self.controller.sum_vnfs_cpu(node)










@register_policy('FIRST_ORDER')
class FirstOrder(Policy):

    def __init__(self, view, controller, **kwargs):
        super(FirstOrder, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {1: 10,  # nat
                    2: 25,  # fw
                    3: 25,  # ids
                    4: 20,  # wanopt
                    5: 20,  # lb
                    6: 25,  # encrypt
                    7: 25,  # decrypts
                    8: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu



    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int) # dict to store the delay taken to run the sfc over the path
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = FirstOrder.sum_vnfs_cpu(sfc) # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v) and v != egress_node:
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf) and vnf_status[vnf] == 0:
                        vnf_status[vnf] = 1
                        self.controller.proc_vnf_payload(u, v)
                        self.controller.vnf_proc(vnf)
                    elif vnf_status[vnf] == 1:
                        continue
                    elif not self.controller.get_vnf(v, vnf):
                        continue
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break

        self.controller.end_session()





@register_policy('GREEDY')
class Greedy(Policy):

    def __init__(self, view, controller, **kwargs):
        super(Greedy, self).__init__(view, controller)


    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {1: 10,  # nat
                    2: 25,  # fw
                    3: 25,  # ids
                    4: 20,  # wanopt
                    5: 20,  # lb
                    6: 25,  # encrypt
                    7: 25,  # decrypts
                    8: 30,  # dpi
                    }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int) # dict to store the delay taken to run the sfc over the path
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = FirstOrder.sum_vnfs_cpu(sfc) # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            delay_sfc[sfc_id] = 0
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            delay_sfc[sfc_id] += self.view.link_delay(u, v)
            if self.view.is_nfv_node(v) and v != egress_node:
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf) and vnf_status[vnf] == 0:
                        vnf_status[vnf] = 1
                        self.controller.proc_vnf_payload(u, v)
                        self.controller.vnf_proc(vnf)
                    elif vnf_status[vnf] == 1:
                        continue
                    elif not self.controller.get_vnf(v, vnf):
                        continue
            delay_sfc[sfc_id] += sum_cpu_sfc
            if all(value == 1 for value in vnf_status.values()) and delay_sfc[sfc_id] <= delay:
                self.controller.sfc_hit(sfc_id)
                break



        self.controller.end_session()


@register_policy('HOD')
class Hod(Policy):

    def __init__(self, view, controller, **kwargs):
        super(Hod, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {1: 10,  # nat
                     2: 25,  # fw
                     3: 25,  # ids
                     4: 20,  # wanopt
                     5: 20,  # lb
                     6: 25,  # encrypt
                     7: 25,  # decrypts
                     8: 30,  # dpi
                }

        sum_vnfs_cpu = 0
        for vnf in vnfs:
            if vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, delay, log):
        delay_sfc = defaultdict(int) # dict to store the delay taken to run the sfc over the path
        missed_vnfs = []
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, delay, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
        sum_cpu_sfc = FirstOrder.sum_vnfs_cpu(sfc) # total time processing of the sfc
        # for u, v in path_links(path):
        for hop in range(1, len(path)):
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            if self.view.is_nfv_node(v) and v != egress_node:
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf):
                        if vnf_status[vnf] == 0:
                            vnf_status[vnf] = 1
                            self.controller.vnf_proc(vnf)
                            self.controller.proc_vnf_payload(u, v)
                        elif vnf_status[vnf] == 1:
                            continue
                        elif not self.controller.get_vnf(v, vnf):
                            continue
                    else:
                        missed_vnfs.append(vnf)

            if len(missed_vnfs) != 0:
                sum_cpu_missed_vnfs = Hod.sum_vnfs_cpu(missed_vnfs)
                nfv_node_min_cpu_all = self.controller.find_nfv_node_with_min_cpu_alloc(ingress_node, egress_node)
                closest_nfv_node = self.controller.get_closest_nfv_node(path)
                # sum_cpu_vnfs_on_node = self.controller.sum_vnfs_cpu_on_node(closest_nfv_node)
                if v == closest_nfv_node: # and v == nfv_node_min_cpu_all:
                    for missed_vnf in missed_vnfs:
                        vnf_status[missed_vnf] = 1
                        self.controller.put_vnf(v, missed_vnf)
                        #self.controller.vnf_proc(missed_vnf)
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
