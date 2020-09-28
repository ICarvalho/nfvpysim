from abc import ABC, abstractmethod
from nfvpysim.util import path_links
from nfvpysim.registry import register_policy


class Policy(ABC):

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
        vnf_status = {}
        for (u, v) in path_links(path):
            self.controller.forward_request_hop(u, v)
            for vnf in sfc:
                vnf_status = {vnf: False for vnf in sfc}
                if self.get_vnf(v, vnf) and vnf_status[vnf] == False: # vnf on node and processed
                    vnf_status[vnf] = True
                    continue
                elif self.get_vnf(v, vnf) and vnf_status[vnf] == True: # vnf has already been processed in previous node
                    continue
                elif not self.get_vnf(v, vnf): # vnf not on node and not processed yet
                    continue
            if all(value == True for value in vnf_status.values() and v == egress_node):
                break
            if self.collector is not None and self.session['log']:
                self.collector.sfc_acc(sfc)
                return True
            else:
                return False

        self.controller.end_session()



@register_policy('GREEDY_WITH_ONLINE_PLACEMENT')
class GreedyWithOnlinePlacementPolicy(Policy):

    def __init__(self, view, controller, **kwargs):
        super(GreedyWithOnlinePlacementPolicy, self).__init__(view, controller)

    def process_event(self, time, ingress_node, egress_node, sfc, log):
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, ingress_node, egress_node, sfc, log)
        vnf_status = {}
        missed_vnfs = []
        for (u, v) in path_links(path):
            self.controller.forward_request_hop(u, v)
            for vnf in sfc:
                vnf_status = {vnf: False for vnf in sfc}
                if self.get_vnf(v, vnf) and vnf_status[vnf] == False: # vnf on node and processed
                    vnf_status[vnf] = True
                    continue
                elif self.get_vnf(v, vnf) and vnf_status[vnf] == True: # vnf has already been processed in previous node
                    continue
                elif not self.get_vnf(v, vnf): # vnf not on node and not processed yet
                    missed_vnfs.append(vnf)
                    continue



from abc import ABC, abstractmethod
from nfvpysim.util import path_links
from nfvpysim.registry import register_policy


class Policy(ABC):

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
        vnf_status = {}
        for (u, v) in path_links(path):
            self.controller.forward_request_hop(u, v)
            for vnf in sfc:
                vnf_status = {vnf: False for vnf in sfc}
                if self.get_vnf(v, vnf) and vnf_status[vnf] == False: # vnf on node and processed
                    vnf_status[vnf] = True
                    continue
                elif self.get_vnf(v, vnf) and vnf_status[vnf] == True: # vnf has already been processed in previous node
                    continue
                elif not self.get_vnf(v, vnf): # vnf not on node and not processed yet
                    continue
            if all(value == True for value in vnf_status.values() and v == egress_node):
                break
            if self.collector is not None and self.session['log']:
                self.collector.sfc_acc(sfc)
                return True
            else:
                return False

        self.controller.end_session()



@register_policy('GREEDY_WITH_ONLINE_PLACEMENT')
class GreedyWithOnlinePlacementPolicy(Policy):

    def __init__(self, view, controller, **kwargs):
        super(GreedyWithOnlinePlacementPolicy, self).__init__(view, controller)

    def process_event(self, time, ingress_node, egress_node, sfc, log):
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, ingress_node, egress_node, sfc, log)
        vnf_status = {}
        missed_vnfs = []
        for (u, v) in path_links(path):
            self.controller.forward_request_hop(u, v)
            for vnf in sfc:
                vnf_status = {vnf: False for vnf in sfc}
                if self.get_vnf(v, vnf) and vnf_status[vnf] == False: # vnf on node and processed
                    vnf_status[vnf] = True
                    continue
                elif self.get_vnf(v, vnf) and vnf_status[vnf] == True: # vnf has already been processed in previous node
                    continue
                elif not self.get_vnf(v, vnf): # vnf not on node and not processed yet
                    missed_vnfs.append(vnf)
                    continue
            if len(missed_vnfs) >= 1 and any(value == False for value in vnf_status.values()):
