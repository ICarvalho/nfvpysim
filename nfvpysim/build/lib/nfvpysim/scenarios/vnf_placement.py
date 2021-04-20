import fnss
import random
from nfvpysim.execution.network import NetworkModelBaseLine, NetworkModelProposal
from nfvpysim.registry import register_vnf_placement
from nfvpysim.registry import CACHE_POLICY




__all__ = ['hod_placement', 'random_placement', 'random_var_len_placement']


@register_vnf_placement('HOD_PLACEMENT')
def hod_placement(topology):
    if not isinstance(topology, fnss.Topology):
        raise ValueError('The topology argument must be an'
                         'instance of fnss.Topology or   of its subclasses')

    #model = NetworkModelProposal(topology, CACHE_POLICY)
    hods_vnfs = [
        [2, 5, 8],
        [3, 5, 6],
        [6, 2, 3],
        [1, 2, 3],
        [5, 2, 1],
        [3, 2, 4, 5],
        [1, 5, 4],
        [4, 6],
    ]

    nfv_nodes = NetworkModelProposal.nfv_cache
    for nfv_node in nfv_nodes:
        vnfs = random.choice(hods_vnfs)
        for vnf in vnfs:
            nfv_nodes[nfv_node].add_vnf(vnf)
            nfv_nodes[nfv_node].list_nfv_cache()
    return nfv_nodes


@register_vnf_placement('RANDOM_PLACEMENT')
def random_placement(topology):
    if not isinstance(topology, fnss.Topology):
        raise ValueError('The topology argument must be an'
                         'instance of fnss.Topology or   of its subclasses')

    #model = NetworkModelBaseLine(topology, CACHE_POLICY)
    vnfs = [1, 2, 3, 4, 5, 6, 7, 8]
    nfv_nodes = NetworkModelProposal.nfv_cache
    for nfv_node in nfv_nodes:
        vnf = random.choice(vnfs)
        nfv_nodes[nfv_node].add_vnf(vnf)
    return nfv_nodes



@register_vnf_placement('RANDOM_VAR_LEN_PLACEMENT')
def random_var_len_placement(topology):
    if not isinstance(topology, fnss.Topology):
        raise ValueError('The topology argument must be an'
                         'instance of fnss.Topology or   of its subclasses')

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
            vnf_sample, cpu = random.choice(list(sfcs.items()))
            if vnf_sample not in var_len_sfc:
                var_len_sfc.append(vnf_sample)
                sfc_len -= 1
                sum_cpu += cpu
                if sum_cpu > 100 or sfc_len == 0:
                    break
                elif sum_cpu <= 100 and sfc_len != 0:
                    sfc_len -= 1

        return var_len_sfc


    #model = NetworkModelBaseLine(topology,CACHE_POLICY)
    nfv_nodes = NetworkModelProposal.nfv_cache
    for nfv_node in nfv_nodes:
        vnfs = var_len_seq_sfc()
        for vnf in vnfs:
            nfv_nodes[nfv_node].add_vnf(vnf)
    return nfv_nodes