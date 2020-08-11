from abc import ABC, abstractmethod
from model.cache import *
from model.cache import *
from model.network import *
from tools.util import path_links, inheritdoc

class Policy(ABC):

    def __init__(self, view, controller, **kwargs):
        self.view = view
        self.controller = controller

    @abstractmethod
    def process_event(self, time, ingress_node, egress_node, sfc, log):

        raise NotImplementedError('The selected policy must implement a process event method')




class FistFit(Policy):

    def __init__(self, view, controller, **kwargs):
        super(FistFit, self).__init__(view, controller)


    def process_event(self, time, ingress_node, egress_node, sfc, log):
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, ingress_node, egress_node, sfc, log)
        for u,v in path_links(path):
            self.controller.forward_request_hop(u,v)
            if self.controller.get_vnf(v, sfc):
                return True
            else:
                self.controller.forward_request_path(v, egress_node)

            break



        self.controller.end_session()








