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
