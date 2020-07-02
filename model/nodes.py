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


class GenerateRandomSfc:

    def generate_seq_vnfs(self):
        sfc = []
        nat = Nat()
        fw = Firewall()
        wanopt = WanOptimizer()
        lb  = LoadBalancer()
        ids = Ids()
        vnfs = [nat, fw, wanopt, lb, ids]
        n = random.randint(1, len(vnfs))
        for i in range(1, n+1):
            vnf = random.choice(vnfs)
            if vnf not in sfc:
                sfc.append(vnf)
        return sfc


class SelectRandomSFC:

    def select_random_sfc(self):
        services = [SFC_01().get_sfc_01(), SFC_02().get_sfc_02(), SFC_03().get_sfc_03(), SFC_04().get_sfc_04(), SFC_05().get_sfc_05(),
                    SFC_06().get_sfc_06(), SFC_07().get_sfc_07(), SFC_08().get_sfc_08(), SFC_09().get_sfc_09(),SFC_10().get_sfc_10()]
        sfc = random.choice(services)
        return sfc




class SFC_01:

    def __init__(self):
        self.sfc_01 = [Nat(), Firewall()]

    def get_sfc_01(self):
        return self.sfc_01


class SFC_02:

    def __init__(self):
        self.sfc_02 = [Nat(), Firewall(), Ids()]

    def get_sfc_02(self):
        return self.sfc_02


class SFC_03:

    def __init__(self):
        self.sfc_03 = [WanOptimizer(), LoadBalancer()]

    def get_sfc_03(self):
        return self.sfc_03


class SFC_04:

    def __init__(self):
        self.sfc_04 = [Firewall(), Ids(), LoadBalancer()]

    def get_sfc_04(self):
        return self.sfc_04


class SFC_05:

    def __init__(self):
        self.sfc_05 = [Nat(), LoadBalancer(), WanOptimizer()]

    def get_sfc_05(self):
        return self.sfc_05


class SFC_06:

    def __init__(self):
        self.sfc_06 = [LoadBalancer(), Firewall(), Nat()]

    def get_sfc_06(self):
        return self.sfc_06

class SFC_07:

    def __init__(self):
        self.sfc_07 = [Firewall(), Ids(), LoadBalancer(), Nat()]

    def get_sfc_07(self):
        return self.sfc_07

class SFC_08:

    def __init__(self):
        self.sfc_08 = [Ids(), Firewall(), LoadBalancer(), WanOptimizer()]

    def get_sfc_08(self):
        return self.sfc_08

class SFC_09:

    def __init__(self):
        self.sfc_09 = [LoadBalancer(), WanOptimizer(), Nat(), Firewall()]

    def get_sfc_09(self):
        return self.sfc_09

class SFC_10:

    def __init__(self):
        self.sfc_10 = [LoadBalancer(), WanOptimizer(), Nat(), Firewall(), Ids()]

    def get_sfc_10(self):
        return self.sfc_10



# nat, fw, wanopt, lb, ids
class RequestPickRandomSFC:

    def __init__(self, ingress_node, egress_node, delay_req):
        self.ingress_node = ingress_node
        self.egress_node = egress_node
        self.sfc =  SelectRandomSFC.select_random_sfc(self)
        self.delay_req = delay_req

class RequestGenerateRandomSFC:

    def __init__(self, ingress_node, egress_node, delay_req):
        self.ingress_node = ingress_node
        self.egress_node = egress_node
        self.sfc = SelectRandomSFC.select_random_sfc(self)
        self.delay_req = delay_req


s = RequestPickRandomSFC('a', 'b', 10)

r = RequestGenerateRandomSFC('a', 'b', 10)
#print(r.sfc)
#print(s.sfc)
p = VnfNode()

#print(r.sfc)
print(r.sfc)
print(p.cpu)
proc = p.proc_request(r)
#print(p.cpu)
print(p.remaining_cpu)





