from __future__ import division
from nfvpysim.registry import register_cache_policy
from collections import deque


__all__ = [
    'NfvCache'
    ]

@register_cache_policy('NFV_CACHE')
class NfvCache:

    def __init__(self, max_size):
        self.nfv_cache = deque(maxlen=int(max_size))
        self.max_size = max_size
        if self.max_size <= 0:
            raise ValueError('max_size must be positive')

    def add_vnf(self, vnf):
        if not self.has_vnf(vnf):
            self.nfv_cache.append(vnf)

    def get_vnf(self, vnf):
        return self.has_vnf(vnf)

    def has_vnf(self, vnf):
        return vnf in self.nfv_cache

    def remove_vnf(self, vnf):
        return self.nfv_cache.remove(vnf)

    def list_nfv_cache(self):
        print(self.nfv_cache)

    def sum_vnfs_cpu_node(self):
        vnfs_cpu =  {0: 15,  # nat
                     1: 25,  # fw
                     2: 25,  # ids
                     3: 20,  # wanopt
                     4: 20,  # lb
                     5: 25,  # encrypt
                     6: 25,  # decrypts
                     7: 30,  # dpi
                     }

        sum_vnfs_cpu = 0
        for vnf in self.nfv_cache:
            if self.has_vnf(vnf) and vnf in vnfs_cpu.keys():
                sum_vnfs_cpu += vnfs_cpu[vnf]
        return sum_vnfs_cpu


"""
c = NfvCache(4)
c.add_vnf(1)
c.add_vnf(2)
c.add_vnf(3)
c.add_vnf(5)

print(c.sum_vnfs_cpu_node())

"""


