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
class FistFit(Policy):

    def __init__(self, view, controller, **kwargs):
        super(FistFit, self).__init__(view, controller)


    def process_event(self, time, ingress_node, egress_node, sfc, log):
        path = self.view.shortest_path(ingress_node, egress_node)
        self.controller.start_session(time, ingress_node, egress_node, sfc, log)
        for (u, v) in path_links(path):





        self.controller.end_session()







