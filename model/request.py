from model.nodes import *


class SFC_01:

    def __init__(self):
        self.id = 'SFC_01'
        self.sfc_01 = [Nat(), Firewall()]

    def get_id(self):
        return self.id

    def get_sfc_01(self):
        return self.sfc_01


class SFC_02:

    def __init__(self):
        self.id = 'SFC_02'
        self.sfc_02 = [Nat(), Firewall(), Ids()]

    def get_id(self):
        return self.id

    def get_sfc_02(self):
        return self.sfc_02


class SFC_03:

    def __init__(self):
        self.id = 'SFC_03'
        self.sfc_03 = [WanOptimizer(), LoadBalancer()]

    def get_id(self):
        return self.id

    def get_sfc_03(self):
        return self.sfc_03


class SFC_04:

    def __init__(self):
        self.id = 'SFC_04'
        self.sfc_04 = [Firewall(), Ids(), LoadBalancer()]

    def get_id(self):
        return self.id

    def get_sfc_04(self):
        return self.sfc_04


class SFC_05:

    def __init__(self):
        self.id = 'SFC_05'
        self.sfc_05 = [Nat(), LoadBalancer(), WanOptimizer()]

    def get_id(self):
        return self.id

    def get_sfc_05(self):
        return self.sfc_05


class SFC_06:

    def __init__(self):
        self.id = 'SFC_06'
        self.sfc_06 = [LoadBalancer(), Firewall(), Nat()]

    def get_id(self):
        return self.id

    def get_sfc_06(self):
        return self.sfc_06

class SFC_07:

    def __init__(self):
        self.id = 'SFC_07'
        self.sfc_07 = [Firewall(), Ids(), LoadBalancer(), Nat()]

    def get_id(self):
        return self.id

    def get_sfc_07(self):
        return self.sfc_07

class SFC_08:

    def __init__(self):
        self.id = 'SFC_08'
        self.sfc_08 = [Ids(), Firewall(), LoadBalancer(), WanOptimizer()]

    def get_id(self):
        return self.id

    def get_sfc_08(self):
        return self.sfc_08

class SFC_09:

    def __init__(self):
        self.id = 'SFC_09'
        self.sfc_09 = [LoadBalancer(), WanOptimizer(), Nat(), Firewall()]

    def get_id(self):
        return self.id

    def get_sfc_09(self):
        return self.sfc_09

class SFC_10:

    def __init__(self):
        self.id = 'SFC_10'
        self.sfc_10 = [LoadBalancer(), WanOptimizer(), Nat(), Firewall(), Ids()]

    def get_id(self):
        return self.id

    def get_sfc_10(self):
        return self.sfc_10



class Request:

    def __init__(self, ingress_node, egress_node, delay_req):
        self.ingress_node = ingress_node
        self.egress_node = egress_node
        self.delay_req = delay_req

    def select_random_sfc(self):
            services = [SFC_01().get_sfc_01(), SFC_02().get_sfc_02(), SFC_03().get_sfc_03(), SFC_04().get_sfc_04(),
                        SFC_05().get_sfc_05(),
                        SFC_06().get_sfc_06(), SFC_07().get_sfc_07(), SFC_08().get_sfc_08(), SFC_09().get_sfc_09(),
                        SFC_10().get_sfc_10()]
            sfc = random.choice(services)
            return sfc

    def generate_seq_vnfs(self):
            sfc = []
            nat = Nat()
            fw = Firewall()
            wanopt = WanOptimizer()
            lb = LoadBalancer()
            ids = Ids()
            vnfs = [nat, fw, wanopt, lb, ids]
            n = random.randint(1, len(vnfs))
            for i in range(1, n + 1):
                vnf = random.choice(vnfs)
                if vnf not in sfc:
                    sfc.append(vnf)
            return sfc



    def random_sfc(self):
            random_sfc = self.select_random_sfc()
            return random_sfc

    def random_var_len_sfc(self):
            var_len_sfc = self.generate_seq_vnfs()
            return var_len_sfc



class GenerateRandomRequest(Request):

    def __init__(self, ingress_node, egress_node, delay_req):
        super().__init__(ingress_node, egress_node, delay_req)
        self.sfc = super().random_sfc()

    def get_sfc(self):
        return self.sfc


class GenerateVarLenRequest(Request):

    def __init__(self, ingress_node, egress_node, delay_req):
        super().__init__(ingress_node, egress_node, delay_req)
        self.sfc = super().random_var_len_sfc()

    def get_sfc(self):
        return self.sfc

"""
rr = GenerateRandomRequest(1, 2, 60)
vr = GenerateVarLenRequest(1, 2, 60)

print(rr.sfc)
print(vr.get_sfc)

"""





