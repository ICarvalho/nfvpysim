from abc import abstractmethod

from nfvpysim.registry import register_policy

# from nfvpysim.util import path_links

__all__ = [
    'Policy',
    'GreedyWithoutPlacement',
    'GreedyWithOnlinePlacementPolicy'
]


class Policy:

    def __init__(self, view, controller, **kwargs):
        self.view = view
        self.controller = controller

    @abstractmethod
    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, log):
        raise NotImplementedError('The selected policy must implement a process event method')


@register_policy('GREEDY_WITHOUT_PLACEMENT')
class GreedyWithoutPlacement(Policy):

    def __init__(self, view, controller, **kwargs):
        super(GreedyWithoutPlacement, self).__init__(view, controller)

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, log):
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, log)
        vnf_status = {vnf: 0 for vnf in sfc}  # 0 - not processed / 1 - processed
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
                    elif not self.controller.get_vnf(v, vnf):
                        continue
            if all(value == 1 for value in vnf_status.values()) and v == egress_node:
                self.controller.sfc_hit(sfc_id)


        self.controller.end_session()


@register_policy('GREEDY_WITH_ONLINE_PLACEMENT')
class GreedyWithOnlinePlacementPolicy(Policy):

    def __init__(self, view, controller, **kwargs):
        super(GreedyWithOnlinePlacementPolicy, self).__init__(view, controller)

    @staticmethod
    def sum_vnfs_cpu(vnfs):
        vnfs_cpu = {1: 15,  # nat
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

    def process_event(self, time, sfc_id, ingress_node, egress_node, sfc, log):
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, sfc_id, ingress_node, egress_node, sfc, log)
        missed_vnfs = []
        vnf_status = {vnf: 0 for vnf in sfc}
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
                        else:
                            continue
                    elif not self.controller.get_vnf(v, vnf):
                        missed_vnfs.append(vnf)

            if len(missed_vnfs) != 0:
                if all(vnf_status[missed_vnf] == 0 for missed_vnf in missed_vnfs):
                    sum_cpu_missed_vnfs = GreedyWithOnlinePlacementPolicy.sum_vnfs_cpu(missed_vnfs)
                    sum_cpu_vnfs_on_node = self.controller.sum_vnfs_cpu_on_node(v)
                    nfv_node_min_cpu_all = self.controller.find_nfv_node_with_min_cpu_alloc(ingress_node, egress_node)
                    closest_nfv_node = self.controller.get_closest_nfv_node(path)
                    if v == closest_nfv_node and v == nfv_node_min_cpu_all: #and sum_cpu_missed_vnfs <= sum_cpu_vnfs_on_node:
                        for missed_vnf in missed_vnfs:
                            vnf_status[missed_vnf] = 1
                            self.controller.put_vnf(v, missed_vnf)
                            self.controller.vnf_proc(missed_vnf)
                            self.controller.proc_vnf_payload(u, v)
                if all(value == 1 for value in vnf_status.values()) and v == egress_node:
                    self.controller.sfc_hit(sfc_id)

        self.controller.end_session()
