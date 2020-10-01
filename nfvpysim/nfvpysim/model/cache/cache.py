from __future__ import division
from nfvpysim import register_cache_policy
from collections import defaultdict



class Dictionary:

    def __init__(self):
        self.items = defaultdict()

    def isEmpty(self):
        return self.items == {}

    def add_item(self, item):
        if not self.has_item(item):
            for key, value in item.items():
                self.items[key] = value

    def remove_item(self, item):
        return self.items.pop(item, None)

    def size(self):
        return len(self.items)

    def get_item_value(self, item):
        return self.items[item]

    def has_item(self, item):
        return item in self.items

    def get_sum_item_values(self):
        return sum(self.items.values())


@register_cache_policy('NFV_CACHE')
class NfvCache:

    def __init__(self, maxlen):
        self._nfvcache = Dictionary()
        self._maxlen = int(maxlen)
        if self._maxlen <= 0:
            raise ValueError('maxlen must be positive')

    def add_vnf(self, vnf):
        return self._nfvcache.add_item(vnf)


    def len_nfv_cache(self):
        return self._nfvcache.size()

    def has_vnf(self, vnf):
        return self._nfvcache.has_item(vnf)

    def get_vnf(self, vnf):
        return self.has_vnf(vnf)

    def remove_vnf(self, vnf):
        return self._nfvcache.remove_item(vnf)

    def get_sum_vnfs_cpu(self):
        return self._nfvcache.get_sum_item_values()

    def get_vnf_cpu_value(self, vnf):
        return self._nfvcache.get_item_value(vnf)



