from nfvpysim.registry import register_workload
import csv
from nfvpysim.scenarios import topology_geant
import random
from nfvpysim.tools import TruncatedZipfDist



__all__ = [
    'StationaryWorkloadRandomSfc',
    'StationaryWorkloadVarLenSfc'
]

@register_workload('STATIONARY_RANDOM_SFC')
class StationaryWorkloadRandomSfc:

    """
    This function generates events on the fly, i.e. instead of creating an
    event schedule to be kept in memory, returns an iterator that generates
    events when needed.

    This is useful for running large schedules of events where RAM is limited
    as its memory impact is considerably lower

    All requests are mapped to receivers uniformly unless a positive *beta*
    parameter is specified


    """

    def __init__(self, topology, n_sfcs, rate=1.0, n_warmup=0, n_measured=4 * 10 ** 5, seed=None):

        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.egress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'egress_node']
        self.sfcs = StationaryWorkloadRandomSfc.generate_random_sfc(n_sfcs)
        self.rate = rate
        self.n_warmup = n_warmup
        self.n_measured = n_measured
        random.seed(seed)


    @staticmethod
    def select_random_sfc():

        services = [
            [1, 2],  # [nat - fw]
            [4, 5],  # [wanopt - lb]
            [1, 2, 3],  # [nat - fw - ids]
            [2, 3, 5],  # [fw - ids - lb]
            [1, 5, 4],  # [nat - lb - wanopt]
            [5, 2, 1],  # [lb - fw - nat]
            [2, 3, 5, 6],  # [fw - ids - lb - encrypt]
            [3, 2, 5, 8],  # [ids - fw - lb - wanopt]
            [5, 4, 6, 2, 3],  # [lb - wanopt - encrypt - fw - ids]
        ]

        return random.choice(services)

    @staticmethod
    def generate_random_sfc(n_sfcs):
        sfcs = []
        for i in range(1, n_sfcs + 1):
            sfc = StationaryWorkloadRandomSfc.select_random_sfc()
            sfcs.append(sfc)

        return sfcs



    def __iter__(self):
        req_counter = 0
        t_event = 0.0
        # header = ['id', 'sfc']
        # with open('random_sfcs.csv', 'w', newline='\n') as f:
            # writer = csv.writer(f)
            # writer.writerow(header)
        while req_counter < self.n_warmup + self.n_measured:
            #for i in range(1, self.n_req-1):
            t_event += (random.expovariate(self.rate))
            ingress_node = random.choice(self.ingress_nodes)
            egress_node = random.choice(self.egress_nodes)
            sfc = random.choice(self.sfcs)
            log = (req_counter >= self.n_warmup)
            event = {'ingress_node': ingress_node, 'egress_node': egress_node, 'sfc': sfc, 'log': log}
            #file_lines = [str(i),',', str(sfc)[1:-1], '\n']
            #f.writelines(file_lines)
            yield (t_event, event)
            req_counter += 1
            #f.close()
        return



@register_workload('STATIONARY_VAR_LEN_SFC')
class StationaryWorkloadVarLenSfc:
    """
    This function generates events on the fly, i.e. instead of creating an
    event schedule to be kept in memory, returns an iterator that generates
    events when needed.

    This is useful for running large schedules of events where RAM is limited
    as its memory impact is considerably lower

    All requests are mapped to receivers uniformly unless a positive *beta*
    parameter is specified


    """

    def __init__(self, topology, n_sfcs, rate=1.0, n_warmup=0, n_measured=4 * 10 ** 5, seed=None):

        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.egress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'egress_node']
        self.sfcs = StationaryWorkloadVarLenSfc.generate_var_len_seq_sfc(n_sfcs)
        self.rate = rate
        self.n_measured = n_measured
        self.n_warmup = n_warmup
        random.seed(seed)


    @staticmethod
    def var_len_seq_sfc():
        var_len_sfc = []
        sfcs = {1: 15,  # nat
                2: 25,  # fw
                3: 25,  # ids
                4: 20,  # wanopt
                5: 20,  # lb
                6: 25,  # encrypt
                7: 25,  # decrypts
                8: 30,  # dpi
                }
        sfc_len = random.randint(1, 8)
        sum_cpu = 0
        while sfc_len != 0:
            vnf, cpu = random.choice(list(sfcs.items()))
            if vnf not in var_len_sfc:
                var_len_sfc.append(vnf)
                sfc_len -= 1
                sum_cpu += cpu
                if sum_cpu > 100 or sfc_len == 0:
                    break
                elif sum_cpu <= 100 and sfc_len != 0:
                    sfc_len -= 1


        return var_len_sfc

    @staticmethod
    def generate_var_len_seq_sfc(n_sfcs):
        sfcs = []
        for i in range(1, n_sfcs + 1):
            sfc = StationaryWorkloadVarLenSfc.var_len_seq_sfc()
            sfcs.append(sfc)

        return sfcs


    def __iter__(self):
        req_counter = 0
        t_event = 0.0
        #header = ['id', 'sfc']
        #with open('var_seq_len_sfc.csv', 'w', newline='\n') as f:
        #writer = csv.writer(f)
        #writer.writerow(header)
        while req_counter < self.n_warmup + self.n_measured:
            #for i in range(0, self.n_req):
            t_event += (random.expovariate(self.rate))
            ingress_node = random.choice(self.ingress_nodes)
            egress_node = random.choice(self.egress_nodes)
            sfc = random.choice(self.sfcs)
            log = (req_counter >= self.n_warmup)
            event = {'ingress_node': ingress_node, 'egress_node': egress_node, 'sfc': sfc, 'log': log}
            #file_lines = [str(i),',', str(sfc)[1:-1], '\n']
            #f.writelines(file_lines)
            yield t_event, event
            req_counter += 1
            #f.close() n_warmup=0,  n_measured=4 * 10 ** 5,
        return


"""
topo= topology_geant()
var_len = StationaryWorkloadRandomSfc(topo, 10*3)

for i in var_len:
    print(i)
"""











"""
services = [
                    [1, 2],  # [nat - fw]
                    [4, 5],  # [wanopt - lb]
                    [1, 2, 3],  # [nat - fw - ids]
                    [2, 3, 5],  # [fw - ids - lb]
                    [1, 5, 4],  # [nat - lb - wanopt]
                    [5, 2, 1],  # [lb - fw - nat]
                    [2, 3, 5, 6],  # [fw - ids - lb - encrypt]
                    [3, 2, 5, 8],  # [ids - fw - lb - wanopt]
                    [5, 4, 6, 2, 3],  # [lb - wanopt - encrypt - fw - ids]
            ]
            
            
sfcs = [{1: 15, 2: 25}, # [nat - fw]
                {4: 20, 5: 20}, # [wanopt - lb]
                {1: 15, 2: 25, 3: 25}, # [nat - fw - ids]
                {2: 25, 3: 25, 5: 20}, # [fw - ids - lb]
                {1: 15, 5: 20, 4: 20}, # [nat - lb - wanopt]
                {5: 20, 2: 25, 1: 15}, # [lb - fw - nat]
                {2: 25, 3: 25, 5: 20, 6: 25}, # [fw - ids - lb - encrypt]
                {3: 25, 2: 25, 5: 20, 8: 30}, # [ids - fw - lb - wanopt]
                {5: 20, 4: 20, 6: 25, 2: 25, 3: 25} # [lb - wanopt - encrypt - fw - ids]
                ]



"""




