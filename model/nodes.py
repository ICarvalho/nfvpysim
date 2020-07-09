import random
from collections import defaultdict

class Vnf:

    def __init__(self, id, name, cpu, ram, bw):

        self.id = id
        self.name = name
        self.cpu = cpu
        self.ram = ram
        self.bw = bw


    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_cpu(self):
        return self.cpu


    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



class Nat(Vnf):

    def __init__(self):
        self.id = 1
        self.name = 'nat'
        self.cpu = 15
        self.ram = 20
        self.bw = 50  # Mbps

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



class Firewall(Vnf):

    def __init__(self):
        self.id = 2
        self.name = 'fw'
        self.cpu = 25
        self.ram = 30
        self.bw = 80 # Mbps

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



class Ids(Vnf):

    def __init__(self):
        self.id = 3
        self.name = 'ids'
        self.cpu = 30
        self.ram = 30
        self.bw = 100 #Mbps

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw


class WanOptimizer(Vnf):

    def __init__(self):
        self.id = 4
        self.name = 'wanopt'
        self.cpu = 20
        self.ram = 25
        self.bw = 90 # Mbps

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



class LoadBalancer(Vnf):

    def __init__(self):
        self.id = 5
        self.name = 'lb'
        self.cpu = 30
        self.ram = 35
        self.bw = 120 # Mbps

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



class Encrypter(Vnf):

    def __init__(self):
        self.id = 6
        self.name = 'encrpt'
        self.cpu = 40
        self.ram = 30
        self.bw = 150 # Mbps

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw


class Decrypter(Vnf):

    def __init__(self):
        self.id = 7
        self.name = 'decrpt'
        self.cpu = 40
        self.ram = 30
        self.bw = 150 # Mbps

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_bw(self):
        return self.bw



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
    vnfs_instances = defaultdict(dict)

    def __init__(self):
        super(VnfNode, self).__init__(id='nfv_node')
        self.cpu = 100
        self.ram = 100
        self.r_cpu = 100
        self.r_ram = 100




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

    def add_vnf_instance(self, vnf):
        self.vnfs_instances[1]['id'] = vnf.get_id()
        self.vnfs_instances['name'] = vnf.get_name()
        self.vnfs_instances['cpu'] = vnf.get_cpu()
        self.vnfs_instances['ram'] = vnf.get_ram()
        self.vnfs_instances['bw'] = vnf.get_bw()




    def get_vnfs_instances(self):
        self.vnfs_instances




nat = Nat()
lb = LoadBalancer()

vnf_node = VnfNode()
vnf_node.add_vnf_instance(nat)
vnf_node.add_vnf_instance(lb)
print(vnf_node.vnfs_instances)


