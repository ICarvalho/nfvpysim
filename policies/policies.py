from abc import ABC, abstractmethod
from model.cache import *
from model.cache import *
from model.network import *

class Policy(ABC):

    def __init__(self, view, controller, topology, **kwargs):
        self.view = view
        self.controller = controller
        self.topology = topology

    @abstractmethod
    def process_event(self, time, ingress_node, request, log):

        raise NotImplementedError('The selected policy must implement a process event method')




class FistFit(Policy):

    def __init__(self, view, controller, topology, **kwargs):
        super(FistFit, self).__init__(view, controller)


    def process_event(self, time, request, log):
        ingress_node = request.ingress_node
        egress_node = request.egress_node
        path = self.view.shortest_path(ingress_node, egress_node)




