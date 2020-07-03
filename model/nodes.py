import random
from collections import defaultdict


class Node:

    def __init__(self, id):
        self.id = id

    def get_node_id(self):
        return self.id




class IngressNode(Node):

    def __init__(self, id='ingress_node'):
        self.id = id

    def get_node_id(self):
        return self.id





class ForwardingNode(Node):

    def __init__(self, id='fw_node'):
        self.id = id

    def get_node_id(self):
        return self.id




class EgressNode(Node):

    def __init__(self, id='egress_node'):
        self.id = id

    def get_node_id(self):
        return self.id



class VnfNode(Node):

    def __init__(self, id='nfv_node'):
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

    def proc_vnf_cpu(self, cpu):
        self.cpu = self.cpu - cpu
        self.remaining_cpu = self.cpu


    def load_vnf_ram(self, ram):
        self.ram = self.ram - ram
        self.remaining_ram = self.ram

    def has_cpu(self):
        if self.remaining_cpu > 0:
            return True

        return False

    def has_ram(self):
        if self.remaining_ram > 0:
            return True

        return False

    def update_vnf_stats(self, vnf):
        vnf = Vnf.get_id()
        self.update_vnf_stats[vnf] += 1




    def proc_request(self, request):

        if not isinstance(request, (RequestPickRandomSFC, RequestGenerateRandomSFC)) :
            raise ValueError('Request must be in the specified format')

        if not self.has_cpu() and not self.has_ram():
            raise ValueError('Not enough cpu and ram for processing the VNF')
        else:

            vnfs_cpu = []
            for vnf in request.sfc:
                proc = self.proc_vnf_cpu(vnf.__getattribute__('cpu'))
                vnfs_cpu.append(proc)

            return vnfs_cpu




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









