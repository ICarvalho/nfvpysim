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

    def __init__(self):
        super(VnfNode, self).__init__(id='nfv_node')
        self.cpu = 100
        self.ram = 100
        self.r_cpu = 100
        self.r_ram = 100
        self._vnfs = defaultdict(dict)




    def get_node_id(self):
        return self.id

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_rem_cpu(self):
        return self.r_cpu

    def get_rem_ram(self):
        return self.ram

    def has_ram(self):
        if self.r_ram > 0:
            return True
        return False


    def proc_vnf(self, cpu_req):
        self.cpu = self.cpu - cpu_req
        self.r_cpu = self.cpu



    def has_ram(self):
        if self.r_ram > 0:
            return True
        return False




    def proc_vnf_on_node(self, vnfs):

        for vnf in vnfs:
            if not self.is_vnf_on_vnf_node(vnf):
                raise ValueError('this vnf is not placed on this node')

            else:
                sum_vnf_cpu = sum(vnf.get_cpu() for vnf in vnfs)
                if sum_vnf_cpu <= self.get_rem_cpu():
                    vnf_cpu = vnf.get_cpu()
                    self.proc_vnf(vnf_cpu)





    def add_vnf_on_vnf_node(self, vnfs):

        for vnf in vnfs:
            if vnf.get_cpu() + self.get_sum_cpu_vnfs() <= self.r_cpu:
                self._vnfs[vnf]['id'] = vnf.get_id()
                self._vnfs[vnf]['name'] = vnf.get_name()
                self._vnfs[vnf]['cpu'] = vnf.get_cpu()
                self._vnfs[vnf]['ram'] = vnf.get_ram()
                self._vnfs[vnf]['bw'] = vnf.get_bw()
        else:
            pass
            #raise ValueError('vnf cannot be placed on the node')


    def get_sum_cpu_vnfs(self):
        return sum(self._vnfs[vnf]['cpu'] for vnf in self._vnfs)




    def is_vnf_on_vnf_node(self, vnf):
        return self._vnfs[vnf]










nat = Nat()
lb = LoadBalancer()
fw = Firewall()
en = Encrypter()

vnfs = [nat, lb, fw]
vnf_node = VnfNode()
vnf_node.add_vnf_on_vnf_node(vnfs)

print(vnf_node._vnfs)
print(vnf_node.get_sum_cpu_vnfs())
print(vnf_node.proc_vnf_on_node(vnfs))
print(vnf_node.get_rem_cpu())




