from __future__ import division
from nfvpysim.registry import register_cache_policy
from collections import deque


__all__ = [
    'NfvCache'
    ]

@register_cache_policy('NFV_CACHE')
class NfvCache:

    def __init__(self, max_size):
        self.nfvcache = deque(maxlen=int(max_size))
        self.max_size = max_size
        if self.max_size <= 0:
            raise ValueError('max_size must be positive')

    def add_vnf(self, vnf):
        if not self.has_vnf(vnf):
            self.nfvcache.append(vnf)

    def get_vnf(self, vnf):
        return self.has_vnf(vnf)

    def has_vnf(self, vnf):
        return vnf in self.nfvcache

    def remove_vnf(self, vnf):
        return self.nfvcache.remove(vnf)

    def list_nfv_cache(self):
        print(self.nfvcache)

    def sum_vnfs_cpu_node(self, node, vnfs):
        vnfs_cpu =  {1: 15,  # nat
                2: 25,  # fw
                3: 25,  # ids
                4: 20,  # wanopt
                5: 20,  # lb
                6: 25,  # encrypt
                7: 25,  # decrypts
                8: 30,  # dpi
                }

        sum_cpu = 0
        for vnf in vnfs:
            if self.has_vnf(vnf) and vnf in vnfs_cpu.keys():
                sum_cpu += vnfs_cpu[vnf]
        return sum_cpu


"""
c = NfvCache(4)
c.add_vnf(1)
c.add_vnf(2)
c.add_vnf(3)
c.add_vnf(4)

print(c.sum_vnfs_cpu_node(1, [1,2,3,4,6]))

"""
