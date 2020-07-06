import random
from collections import defaultdict


class Node:

    def __init__(self, id):
        self.id = id

    def get_node_id(self):
        return self.id




class IngressNode(Node):

    def __init__(self):
        super(IngressNode, self).__init__(id='ingress_node')






class ForwardingNode(Node):

    def __init__(self):
        super(ForwardingNode, self).__init__(id='forwarding_node')




class EgressNode(Node):

    def __init__(self):
        super(EgressNode, self).__init__(id='egress_node')



class VnfNode(Node):

    def __init__(self):
        super(VnfNode, self).__init__(id='nfv_node')
        self.id = id
        self.cpu = 100
        self.ram = 100
        self.remaining_cpu = 100
        self.remaining_ram = 100
        self.handle_vnf = False
        self.vnf_counter = defaultdict(int)


    def get_node_id(self):
        return self.id


    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_rem_cpu(self):
        return self.remaining_cpu

    def get_rem_ram(self):
        return self.remaining_ram

    def has_ram(self):
        if self.remaining_ram > 0:
            return True

        return False



    def proc_vnf_cpu(self, cpu_req):
        self.cpu = self.cpu - cpu_req
        self.remaining_cpu = self.cpu


    def load_vnf_ram(self, ram_req):
        self.ram = self.ram - ram_req
        self.remaining_ram = self.ram


    def has_cpu(self):
        if self.remaining_cpu > 0:
            return True
        return False

    def has_ram(self):
        if self.remaining_ram > 0:
            return True
        return False




class Vnf:

    def __init__(self, id, cpu, ram, bw):

        self.id = id
        self.cpu = cpu
        self.ram = ram
        self.bw = bw


    def get_id(self):
        return self.id

    def get_cpu(self):
        return self.cpu


    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



class Nat(Vnf):

    def __init__(self):
        self.id = 'nat'
        self.cpu = 15
        self.ram = 20
        self.bw = 50  # Mbps


    def get_id(self):
        return self.id

    def get_cpu(self):
        return self.cpu


    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



class Firewall(Vnf):

    def __init__(self):
        self.id = 'fw'
        self.cpu = 25
        self.ram = 30
        self.bw = 80 # Mbps

    def get_id(self):
        return self.id

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



class Ids(Vnf):

    def __init__(self):
        self.id = 'ids'
        self.cpu = 30
        self.ram = 30
        self.bw = 100 #Mbps

    def get_id(self):
        return self.id

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw


class WanOptimizer(Vnf):

    def __init__(self):
        self.id = 'wanopt'
        self.cpu = 20
        self.ram = 25
        self.bw = 90 # Mbps

    def get_id(self):
        return self.id

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



class LoadBalancer(Vnf):

    def __init__(self):
        self.id = 'lb'
        self.cpu = 20
        self.ram = 20
        self.bw = 120 # Mbps

    def get_id(self):
        return self.id

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw









