from abc import abstractmethod

from nfvpysim.registry import register_policy
#from nfvpysim.util import path_links

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
    def process_event(self, time, ingress_node, egress_node, sfc, log):

        raise NotImplementedError('The selected policy must implement a process event method')



@register_policy('GREEDY_WITHOUT_PLACEMENT')
class GreedyWithoutPlacement(Policy):

    def __init__(self, view, controller, **kwargs):
        super(GreedyWithoutPlacement, self).__init__(view, controller)
    def process_event(self, time, ingress_node, egress_node, sfc, log):
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, ingress_node, egress_node, sfc, log)
        vnf_status = {vnf: False for vnf in sfc}
        #for u, v in path_links(path):
        for hop in range(1, len(path)):
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf) and vnf_status[vnf] is False: # vnf on node and processed
                        vnf_status[vnf] = True
                        self.controller.vnf_proc(vnf)
                        self.controller.proc_vnf_payload(u, v)
                    elif self.controller.get_vnf(v, vnf) and vnf_status[vnf] is True:
                        continue
                    elif not self.controller.get_vnf(v, vnf) and vnf_status[vnf] is False:
                        continue
            if all(value is True for value in vnf_status.values())and v == egress_node:
                break

                #print(vnf_status)
                #self.controller.sfc_hit(sfc)

        self.controller.end_session()



@register_policy('GREEDY_WITH_ONLINE_PLACEMENT')
class GreedyWithOnlinePlacementPolicy(Policy):

    def __init__(self, view, controller, **kwargs):
        super(GreedyWithOnlinePlacementPolicy, self).__init__(view, controller)

    def process_event(self, time, ingress_node, egress_node, sfc, log):
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, ingress_node, egress_node, sfc, log)
        missed_vnfs = []
        vnf_status = {vnf: False for vnf in sfc}
        #for u, v in path_links(path):
        for hop in range(1, len(path)):
            u = path[hop - 1]
            v = path[hop]
            self.controller.forward_request_vnf_hop(u, v)
            if self.view.is_nfv_node(v):
                for vnf in sfc:
                    if self.controller.get_vnf(v, vnf) and vnf_status[vnf] is False: # vnf on node and processed
                        vnf_status[vnf] = True
                        self.controller.vnf_proc(vnf)
                        self.controller.proc_vnf_payload(u, v)
                    elif self.controller.get_vnf(v, vnf) and vnf_status[vnf] is True:
                        continue
                    elif not self.controller.get_vnf(v, vnf) and vnf_status[vnf] is False: # vnf not on node and not processed yet
                        missed_vnfs.append(vnf)

            if len(missed_vnfs) != 0 and v != egress_node :
                if any(missed_vnf in vnf_status.keys() and vnf_status[missed_vnf] is False for missed_vnf in missed_vnfs):
                    target_nfv_node = self.controller.find_target_nfv_node(path, missed_vnfs)
                    closest_nfv_node = self.controller.get_closest_nfv_node(path)
                    if v == closest_nfv_node and v == target_nfv_node and v != egress_node:
                        for missed_vnf in missed_vnfs:
                            self.controller.put_vnf(v, missed_vnf)
                            self.controller.vnf_proc(missed_vnf)
                            self.controller.proc_vnf_payload(u, v)
                            vnf_status[missed_vnf] = True
                if all(value is True for value in vnf_status.values()) and v == egress_node:
                    break
            #if self.collector is not None and self.session['log']:
                #self.collector.sfc_acc(sfc)
                #return True
            #else:
                #return False

        self.controller.end_session()
