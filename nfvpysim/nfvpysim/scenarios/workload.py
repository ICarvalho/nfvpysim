from nfvpysim.registry import register_workload
from nfvpysim.scenarios.topology import *
from nfvpysim.scenarios.requests import *
import math
import csv
import random



__all__ = [
    'StationaryWorkloadSfcByLen',
    'StationaryWorkloadVarLenSfc',
    'StationaryWorkloadRandomSfc',
    'TraceDrivenWorkload'
]


def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def generate_uniform_delay(lower, upper):
    delay = random.uniform(lower, upper)
    return round(delay, 2)


def get_uniform_delay_sfc(sfc):
    sfcs_delay = {
         1: generate_uniform_delay(10, 15),  # nat
         2: generate_uniform_delay(20, 25),  # fw
         3: generate_uniform_delay(20, 25),  # ids
         4: generate_uniform_delay(15, 20),  # wanopt
         5: generate_uniform_delay(15, 20),  # lb
         6: generate_uniform_delay(20, 25),  # encrypt
         7: generate_uniform_delay(20, 25),  # decrypts
         8: generate_uniform_delay(25, 30),  # dpi

    }
    delay_sfc = 0
    for vnf in sfc:
        if vnf in sfcs_delay.keys():
            delay_sfc += sfcs_delay[vnf]

    return delay_sfc




def get_delay(service):

    dict_services = {

        1: {'sfc': [1, 2, 3], 'delay': 120},
        2: {'sfc': [1, 5, 4], 'delay': 100},
        3: {'sfc': [2, 3, 5, 6], 'delay': 200},
        4: {'sfc': [3, 2, 5, 8], 'delay': 200},
        5: {'sfc': [3, 5, 6, 7], 'delay': 250},
        6: {'sfc': [3, 5, 2, 3, 4], 'delay': 300},
        7: {'sfc': [5, 4, 6, 2, 3], 'delay': 300},
        8: {'sfc': [3, 5, 6, 7, 8], 'delay': 320},

    }
    for k, v in dict_services.items():
        for k1, v1 in v.items():
            if v1 == service:
                return v.get('delay', v)


@register_workload('STATIONARY_SFC_BY_LEN')
class StationaryWorkloadSfcByLen:

    """
    This function generates events on the fly, i.e. instead of creating an
    event schedule to be kept in memory, returns an iterator that generates
    events when needed.

    This is useful for running large schedules of events where RAM is limited
    as its memory impact is considerably lower

    All requests are mapped to receivers uniformly unless a positive *beta*
    parameter is specified


    """

    def __init__(self, topology, sfc_len, sfc_req_rate=1.0, n_warmup= 0, n_measured= 1* 10 ** 4, seed=None, **kwargs):
        self.sfc_len = sfc_len
        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.egress_nodes =  [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'egress_node']
        self.sfc_req_rate = sfc_req_rate
        self.n_warmup = n_warmup
        self.n_measured = n_measured
        random.seed(seed)


    def __iter__(self):
        req_counter = 0
        t_event = 0.0
        header = ['id', 'sfc']
        with open('random_sfc_by_len.csv', 'w', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            while req_counter < self.n_warmup + self.n_measured:
                for i in range(1, self.n_measured + 1):
                    t_event += (random.expovariate(self.sfc_req_rate))
                    ingress_node = random.choice(self.ingress_nodes)
                    egress_node = random.choice(self.egress_nodes)
                    self.req = RequestSfcByLen()
                    self.sfc = self.req.gen_sfc_by_len(self.sfc_len)
                    delay = get_uniform_delay_sfc(self.sfc)
                    sfc_id = truncate(t_event, 2)
                    log = (req_counter >= self.n_warmup)
                    event = {'sfc_id': sfc_id, 'ingress_node': ingress_node, 'egress_node': egress_node, 'sfc': self.sfc, 'delay': delay, 'log': log}
                    #file_lines = [str(sfc)[1:-1], '\n'] #str(i),',',
                    #f.writelines(file_lines)
                    yield t_event, event
                    req_counter += 1
                f.close()
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

    def __init__(self, topology, sfc_req_rate =1.0, n_warmup=0, n_measured=4 * 10 ** 5, seed=None):

        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.egress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'egress_node']
        self.rate = sfc_req_rate
        self.n_measured = n_measured
        self.n_warmup = n_warmup
        random.seed(seed)



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
            self.req = RequestVarLenSfc()
            self.sfc = self.req.var_len_seq_sfc()
            delay = get_uniform_delay_sfc(self.sfc)
            sfc_id = truncate(t_event, 2)
            log = (req_counter >= self.n_warmup)
            event = {'sfc_id': sfc_id, 'ingress_node': ingress_node, 'egress_node': egress_node, 'sfc': self.sfc, 'delay': delay, 'log': log}
            #file_lines = [str(i),',', str(sfc)[1:-1], '\n']
            #f.writelines(file_lines)
            yield t_event, event
            req_counter += 1
            #f.close() n_warmup=0,  n_measured=4 * 10 ** 5,
        return


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

    def __init__(self, topology, sfc_req_rate, n_warmup, n_measured=20**1, seed=None):

        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.egress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'egress_node']
        self.sfc_req_rate = sfc_req_rate
        self.n_measured = n_measured
        self.n_warmup = n_warmup
        random.seed(seed)



    def __iter__(self):
        req_counter = 0
        t_event = 0.0

        #header = ['id', 'sfc']
        #with open('var_seq_len_sfc.csv', 'w', newline='\n') as f:
        #writer = csv.writer(f)
        #writer.writerow(header)


        while req_counter < self.n_warmup + self.n_measured:
            #for i in range(0, self.n_req):
            t_event += (random.expovariate(self.sfc_req_rate))
            ingress_node = random.choice(self.ingress_nodes)
            egress_node = random.choice(self.egress_nodes)
            req = RequestRandomSfc()
            self.sfc = req.select_random_sfc()
            #delay = get_delay(self.sfc)
            if delay is None:
                continue
            sfc_id = truncate(t_event, 2)
            log = (req_counter >= self.n_warmup)
            event = {'sfc_id': sfc_id, 'ingress_node': ingress_node, 'egress_node': egress_node, 'sfc': self.sfc, 'delay': delay, 'log': log}
            #file_lines = [str(i),',', str(sfc)[1:-1], '\n']
            #f.writelines(file_lines)
            yield (t_event, event)
            req_counter += 1
            #f.close() n_warmup=0,  n_measured=4 * 10 ** 5,
        return



@register_workload('TRACE_DRIVEN')
class TraceDrivenWorkload:
    def __init__(self, topology, n_warmup, n_measured,
                 sfc_reqs_file='/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/sfc_test_data.csv', rate=1.0, **kwargs):
        # Set high buffering to avoid one-line reads
        self.buffering = 64 * 1024 * 1024
        self.n_warmup = n_warmup
        self.n_measured = n_measured
        self.sfc_reqs_file = sfc_reqs_file
        self.rate = rate
        self.ingress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'ingress_node']
        self.egress_nodes = [v for v in topology.nodes() if topology.node[v]['stack'][0] == 'egress_node']


    def __iter__(self):
        req_counter = 0
        t_event = 0.0
        with open(self.sfc_reqs_file, 'r', buffering=self.buffering) as sfc_file:
            for sfc in sfc_file:
                t_event += (random.expovariate(self.rate))
                ingress_node= random.choice(self.ingress_nodes)
                egress_node = random.choice(self.egress_nodes)
                sfc_id = truncate(t_event, 2)
                log = (req_counter >= self.n_warmup)
                event = {'sfc_id': sfc_id, 'ingress_node': ingress_node, 'egress_node': egress_node, 'sfc': sfc, 'log': log}
                yield t_event, event
                req_counter += 1
                if req_counter >= self.n_warmup + self.n_measured:
                    return
            raise ValueError("Trace did not contain enough requests")



#topo = topology_tatanld()
#r = StationaryWorkloadRandomSfc(topo, 10**5, 0)
#for i in r:
    #print(i)






















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




