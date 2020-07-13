from model.vnfs import*
from collections import defaultdict


class VnfNode:


    def __init__(self):
        self.id = 'nfv_node'
        self.cpu = 100
        self.ram = 100
        self.r_cpu = 100
        self.r_ram = 100
        self._vnfs =defaultdict(dict)



    def add_vnf(self, vnf):
        if vnf in self._vnfs:
            print('vnf is already on the node')
        else:
            self._vnfs[vnf]['id'] = vnf.get_id()
            self._vnfs[vnf]['name'] = vnf.get_name()
            self._vnfs[vnf]['cpu'] = vnf.get_cpu()
            self._vnfs[vnf]['ram'] = vnf.get_ram()
            self._vnfs[vnf]['bw'] = vnf.get_bw()
        return self._vnfs




    def get_node_id(self):
        return self.id


    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_rem_cpu(self):
        return self.r_cpu

    def get_rem_ram(self):
        return self.r_ram


    def proc_vnf_cpu(self, vnf):
        if vnf in self._vnfs:
            vnf_cpu = self._vnfs[vnf]['cpu']
            self.cpu = self.cpu - vnf_cpu
            self.r_cpu = self.cpu
            return self.cpu
        else:
            print('vnf is not instantiated on the node')


    def load_vnf_ram(self, vnf):
        if vnf in self._vnfs:
            vnf_ram = self._vnfs[vnf]['ram']
            self.ram = self.ram - vnf_ram
            self.r_ram = self.ram
            return self.ram
        else:
            print('vnf is not instantiated on the node')



    def has_cpu(self):
        if self.r_cpu > 0:
            return True
        return False

    def has_ram(self):
        if self.r_ram > 0:
            return True
        return False
"""

node = VnfNode()
nat = Nat()
fw = Firewall()
lb = LoadBalancer()
node.add_vnf(nat)
node.add_vnf(fw)
node.add_vnf(lb)
proc = node.proc_vnf_cpu(fw)
print(node._vnfs)
r = node.load_vnf_ram(fw)
print(node.has_ram())
"""



