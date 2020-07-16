from model.vnfs import*
from collections import defaultdict


class VnfNode:


    def __init__(self):
        self.id = 'nfv_node'
        self.cpu = 100
        self.ram = 100
        self.r_cpu = 100
        self.r_ram = 100
        self._vnfs = defaultdict(dict)


    @staticmethod
    def add_vnf(self, vnf):

        vnf_cpu = getattr(vnf, 'cpu')
        if self.sum_vnfs_cpu() + vnf_cpu > 100:
            raise ValueError('The vnf cannot be added to this node')
        else:
            if getattr(vnf, 'cpu')  <= self.get_rem_cpu():
                if vnf in self.vnfs:
                    print('this vnf is already on the node')
                else:
                    self._vnfs[vnf]['id'] = vnf.get_node_id()
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

    def get_vnfs(self):
        return self._vnfs


    def proc_vnf_cpu(self, vnf):
        if vnf in self._vnfs:
            vnf_cpu = self._vnfs[vnf]['cpu']
            self.cpu = self.cpu - vnf_cpu
            self.r_cpu = self.cpu

        else:
            print('vnf is not instantiated on the node')


    def load_vnf_ram(self, vnf):
        if vnf in self._vnfs:
            vnf_ram = self._vnfs[vnf]['ram']
            self.ram = self.ram - vnf_ram
            self.r_ram = self.ram

        else:
            print('vnf is not instantiated on the node')



    def sum_vnfs_cpu(self):
        sum = 0
        for key, value in self._vnfs.items():
            if value and 'cpu' in value.keys():
                sum += value['cpu']

        return sum

    @property
    def vnfs(self):
        return self._vnfs


"""
node = VnfNode()
nat = Nat()
fw = Firewall()
en = Encrypter()
lb = LoadBalancer()
node.add_vnf(nat)
node.add_vnf(fw)
node.add_vnf(en)


print(node.get_rem_cpu())
sum = node.sum_vnfs_cpu()

proc_fw = node.proc_vnf_cpu(fw)
proc_nat = node.proc_vnf_cpu(nat)
#proc_en_nat = node.proc_vnf_cpu(en)
proc_lb = node.proc_vnf_cpu(en)
print(node.get_rem_cpu())


print(node._vnfs)
print('remaining cpu: ', node.get_rem_cpu())
print('sum of vnfs: ',  sum)


"""



