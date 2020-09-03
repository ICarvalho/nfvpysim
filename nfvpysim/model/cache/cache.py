from __future__ import division
from nfvpysim.registry import register_cache_policy
from nfvpysim.util import apportionment, inheritdoc




class Deque:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
        else:
            pass

    def add_items(self, items):
        for item in items:
            if item not in self.items:
                self.items.append(item)
            else:
                pass

    def remove_item(self, item):
        if item not in self.items:
            pass
        else:
            return self.items.remove(item)

    def size(self):
        return len(self.items)

    def has_item(self, item):
        return item in self.items


@register_cache_policy('NFV_CACHE')
class NfvCache:

    def __init__(self, maxlen, **kwargs):
        self._nfvcache = Deque()
        self._maxlen = int(maxlen)
        if self._maxlen <= 0:
            raise ValueError('maxlen must be positive')

    def add_vnf(self, vnf):
        return self._nfvcache.add_item(vnf)

    def add_vnfs(self, vnfs):
        return self._nfvcache.add_items(vnfs)

    def len_nfv_cache(self):
        return self._nfvcache.size()

    def has_vnf(self, vnf):
        return self._nfvcache.has_item(vnf)

    def get_vnf(self, vnf):
        return self.has_vnf(vnf)

    def remove_vnf(self, vnf):
        return self._nfvcache.remove_item(vnf)



