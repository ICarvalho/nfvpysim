from model.nodes import *
import random


class SFC_01:

    def __init__(self):
        self.id = 'SFC_01'
        self.sfc_01 = [Nat(), Firewall()]


    def get_id(self):
        return self.id

    def get_sfc_01(self):
        return self.sfc_01

    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_01:
            vnfs_id.append(i.get_id())
        return vnfs_id


class SFC_02:

    def __init__(self):
        self.id = 'SFC_02'
        self.sfc_02 = [Nat(), Firewall(), Ids()]

    def get_id(self):
        return self.id

    def get_sfc_02(self):
        return self.sfc_02

    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_02:
            vnfs_id.append(i.get_id())
        return vnfs_id


class SFC_03:

    def __init__(self):
        self.id = 'SFC_03'
        self.sfc_03 = [WanOptimizer(), LoadBalancer()]

    def get_id(self):
        return self.id

    def get_sfc_03(self):
        return self.sfc_03

    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_03:
            vnfs_id.append(i.get_id())
        return vnfs_id


class SFC_04:

    def __init__(self):
        self.id = 'SFC_04'
        self.sfc_04 = [Firewall(), Ids(), LoadBalancer()]

    def get_id(self):
        return self.id

    def get_sfc_04(self):
        return self.sfc_04

    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_04:
            vnfs_id.append(i.get_id())
        return vnfs_id


class SFC_05:

    def __init__(self):
        self.id = 'SFC_05'
        self.sfc_05 = [Nat(), LoadBalancer(), WanOptimizer()]

    def get_id(self):
        return self.id

    def get_sfc_05(self):
        return self.sfc_05

    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_05:
            vnfs_id.append(i.get_id())
        return vnfs_id


class SFC_06:

    def __init__(self):
        self.id = 'SFC_06'
        self.sfc_06 = [LoadBalancer(), Firewall(), Nat()]

    def get_id(self):
        return self.id

    def get_sfc_06(self):
        return self.sfc_06

    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_06:
            vnfs_id.append(i.get_id())
        return vnfs_id



class SFC_07:

    def __init__(self):
        self.id = 'SFC_07'
        self.sfc_07 = [Firewall(), Ids(), LoadBalancer(), Encrypter()]

    def get_id(self):
        return self.id

    def get_sfc_07(self):
        return self.sfc_07

    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_07:
            vnfs_id.append(i.get_id())
        return vnfs_id

class SFC_08:

    def __init__(self):
        self.id = 'SFC_08'
        self.sfc_08 = [Ids(), Firewall(), LoadBalancer(), WanOptimizer()]

    def get_id(self):
        return self.id

    def get_sfc_08(self):
        return self.sfc_08

    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_08:
            vnfs_id.append(i.get_id())
        return vnfs_id

class SFC_09:

    def __init__(self):
        self.id = 'SFC_09'
        self.sfc_09 = [LoadBalancer(), WanOptimizer(), Nat(), Firewall(), Encrypter(), Decrypter()]

    def get_id(self):
        return self.id

    def get_sfc_09(self):
        return self.sfc_09

    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_09:
            vnfs_id.append(i.get_id())
        return vnfs_id

class SFC_10:

    def __init__(self):
        self.id = 'SFC_10'
        self.sfc_10 = [LoadBalancer(), WanOptimizer(), Encrypter(), Firewall(), Ids()]

    def get_id(self):
        return self.id

    def get_sfc_10(self):
        return self.sfc_10


    def get_vnfs_id(self):
        vnfs_id = []
        for i in self.sfc_10:
            vnfs_id.append(i.get_id())
        return vnfs_id




class GenerateSfcs:



    def select_random_sfc(self):

        services = [SFC_01().get_sfc_01(), SFC_02().get_sfc_02(), SFC_03().get_sfc_03(), SFC_04().get_sfc_04(),
                    SFC_05().get_sfc_05(),
                    SFC_06().get_sfc_06(), SFC_07().get_sfc_07(), SFC_08().get_sfc_08(), SFC_09().get_sfc_09(),
                    SFC_10().get_sfc_10()]
        sfc = random.choice(services)
        #sfcs = self.get_vnfs_id(sfc)
        return sfc



    def generate_seq_vnfs(self):
        sfc = []
        nat = Nat()
        fw = Firewall()
        wanopt = WanOptimizer()
        lb = LoadBalancer()
        ids = Ids()
        encr = Encrypter()
        decr = Decrypter()
        vnfs = [nat, fw, wanopt, lb, ids, encr, decr]
        n = random.randint(1, len(vnfs))
        for i in range(1, n + 1):
            vnf = random.choice(vnfs)
            if vnf not in sfc:
                sfc.append(vnf)
           # sfcs = self.get_vnfs_id(sfc)
        return sfc


    def get_vnfs_id(self, sfc):
        vnf_list = []
        for i in sfc:
            vnf_list.append(i.get_id())
        return vnf_list



class RequestRandomSfc:

    def __init__(self):

        self.sfc = GenerateSfcs().select_random_sfc()


    def get_sfc(self):

        return self.sfc



    def get_vnfs_id(self, sfc):
        vnf_list = []
        for i in sfc:
            vnf_list.append(i.get_id())
        return vnf_list


class RequestVarLenSFc:

    def __init__(self):

        self.sfc = GenerateSfcs().generate_seq_vnfs()


    def get_sfc(self):
        return self.sfc


    def get_vnfs_id(self, sfc):
        vnf_list = []
        for i in sfc:
            vnf_list.append(i.get_id())
        return vnf_list




"""
req_01  = RequestVarLenSFc()
req_02 = RequestRandomSfc()


print(req_01.get_sfc())
print(req_01.get_vnfs_id(req_01.get_sfc()))
print(req_02.get_sfc())


"""














