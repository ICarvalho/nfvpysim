from __future__ import division

import numpy as np
import abc
from collections import deque
from nfvpysim.registry import register_cache_policy
from nfvpysim.util import apportionment, inheritdoc

class LinkedSet(object):
    """A doubly-linked set, i.e., a set whose entries are ordered and stored
    as a doubly-linked list.
    This data structure is designed to efficiently implement a number of cache
    replacement policies such as LRU and derivatives such as Segmented LRU.
    It provides O(1) time complexity for the following operations: searching,
    remove from any position, move to top, move to bottom, insert after or
    before a given item.
    """
    class _Node(object):
        """Class implementing a node of the linked list"""

        def __init__(self, val, up=None, down=None):
            """Constructor
            Parameters
            ----------
            val : any hashable type
                The value stored by the node
            up : any hashable type, optional
                The node above in the list
            down : any hashable type, optional
                The node below in the list
            """
            self.val = val
            self.up = up
            self.down = down

    def __init__(self, iterable=[]):
        """Constructor
        Parameters
        ----------
        itaerable : iterable type
            An iterable type to inizialize the data structure.
            It must contain only one instance of each element
        """
        self._top = None
        self._bottom = None
        self._map = {}
        if iterable:
            if len(set(iterable)) < len(iterable):
                raise ValueError('The iterable parameter contains repeated '
                                 'elements')
            for i in iterable:
                self.append_bottom(i)

    def __len__(self):
        """Return the number of elements in the linked set
        Returns
        -------
        len : int
            The length of the set
        """
        return len(self._map)

    def __iter__(self):
        """Return an iterator over the set
        Returns
        -------
        reversed : iterator
            An iterator over the set
        """
        cur = self._top
        while cur:
            yield cur.val
            cur = cur.down

    def __reversed__(self):
        """Return a reverse iterator over the set
        Returns
        -------
        reversed : iterator
            A reverse iterator over the set
        """
        cur = self._bottom
        while cur:
            yield cur.val
            cur = cur.up

    def __str__(self):
        """Return a string representation of the set
        Returns
        -------
        str : str
            A string representation of the set
        """
        return self.__class__.__name__ + "([" + "".join("%s, " % str(i) for i in self)[:-2] + "])"

    def __contains__(self, k):
        """Return whether the set contains a given item
        Parameters
        ----------
        k : any hashable type
            The item to search
        Returns
        -------
        contains : bool
            *True* if the set contains the item, *False* otherwise
        """
        return k in self._map

    @property
    def top(self):
        """Return the item at the top of the set
        Returns
        -------
        top : any hashable type
            The item at the top or *None* if the set is empty
        """
        return self._top.val if self._top is not None else None

    @property
    def bottom(self):
        """Return the item at the bottom of the set
        Returns
        -------
        bottom : any hashable type
            The item at the bottom or *None* if the set is empty
        """
        return self._bottom.val if self._bottom is not None else None

    def pop_top(self):
        """Pop the item at the top of the set
        Returns
        -------
        top : any hashable type
            The item at the top or *None* if the set is empty
        """
        if self._top is None:  # No elements to pop
            return None
        k = self._top.val
        if self._top == self._bottom:  # One single element
            self._bottom = self._top = None
        else:
            self._top.down.up = None
            self._top = self._top.down
        self._map.pop(k)
        return k

    def pop_bottom(self):
        """Pop the item at the bottom of the set
        Returns
        -------
        bottom : any hashable type
            The item at the bottom or *None* if the set is empty
        """
        if self._bottom is None:  # No elements to pop
            return None
        k = self._bottom.val
        if self._bottom == self._top:  # One single element
            self._top = self._bottom = None
        else:
            self._bottom.up.down = None
            self._bottom = self._bottom.up
        self._map.pop(k)
        return k

    def append_top(self, k):
        """Append an item at the top of the set
        Parameters
        ----------
        k : any hashable type
            The item to append
        """
        if k in self._map:
            raise KeyError('The item %s is already in the set' % str(k))
        n = self._Node(val=k, up=None, down=self._top)
        if self._top == self._bottom is None:
            self._bottom = n
        else:
            self._top.up = n
        self._top = n
        self._map[k] = n

    def append_bottom(self, k):
        """Append an item at the bottom of the set
        Parameters
        ----------
        k : any hashable type
            The item to append
        """
        if k in self._map:
            raise KeyError('The item %s is already in the set' % str(k))
        n = self._Node(val=k, up=self._bottom, down=None)
        if self._top == self._bottom is None:
            self._top = n
        else:
            self._bottom.down = n
        self._bottom = n
        self._map[k] = n

    def move_up(self, k):
        """Move a specified item one position up in the set
        Parameters
        ----------
        k : any hashable type
            The item to move up
        """
        if k not in self._map:
            raise KeyError('Item %s not in the set' % str(k))
        n = self._map[k]
        if n.up is None:  # already on top or there is only one element
            return
        if n.down is None:  # bottom but not top: there are at least two elements
            self._bottom = n.up
        else:
            n.down.up = n.up
        n.up.down = n.down
        new_up = n.up.up
        new_down = n.up
        if new_up:
            new_up.down = n
        else:
            self._top = n
        new_down.up = n
        n.up = new_up
        n.down = new_down

    def move_down(self, k):
        """Move a specified item one position down in the set
        Parameters
        ----------
        k : any hashable type
            The item to move down
        """
        if k not in self._map:
            raise KeyError('Item %s not in the set' % str(k))
        n = self._map[k]
        if n.down is None:  # already at the bottom or there is only one element
            return
        if n.up is None:
            self._top = n.down
        else:
            n.up.down = n.down
        n.down.up = n.up
        new_down = n.down.down
        new_up = n.down
        new_up.down = n
        if new_down is not None:
            new_down.up = n
        else:
            self._bottom = n
        n.up = new_up
        n.down = new_down

    def move_to_top(self, k):
        """Move a specified item to the top of the set
        Parameters
        ----------
        k : any hashable type
            The item to move to the top
        """
        if k not in self._map:
            raise KeyError('Item %s not in the set' % str(k))
        n = self._map[k]
        if n.up is None:  # already on top or there is only one element
            return
        if n.down is None:  # at the bottom, there are at least two elements
            self._bottom = n.up
        else:
            n.down.up = n.up
        n.up.down = n.down
        # Move to top
        n.up = None
        n.down = self._top
        self._top.up = n
        self._top = n

    def move_to_bottom(self, k):
        """Move a specified item to the bottom of the set
        Parameters
        ----------
        k : any hashable type
            The item to move to the bottom
        """
        if k not in self._map:
            raise KeyError('Item %s not in the set' % str(k))
        n = self._map[k]
        if n.down is None:  # already at bottom or there is only one element
            return
        if n.up is None:  # at the top, there are at least two elements
            self._top = n.down
        else:
            n.up.down = n.down
        n.down.up = n.up
        # Move to top
        n.down = None
        n.up = self._bottom
        self._bottom.down = n
        self._bottom = n

    def insert_above(self, i, k):
        """Insert an item one position above a given item already in the set
        Parameters
        ----------
        i : any hashable type
            The item of the set above which the new item is inserted
        k : any hashable type
            The item to insert
        """
        if k in self._map:
            raise KeyError('Item %s already in the set' % str(k))
        if i not in self._map:
            raise KeyError('Item %s not in the set' % str(i))
        n = self._map[i]
        if n.up is None:  # Insert on top
            return self.append_top(k)
        # Now I know I am inserting between two actual elements
        m = self._Node(k, up=n.up, down=n)
        n.up.down = m
        n.up = m
        self._map[k] = m

    def insert_below(self, i, k):
        """Insert an item one position below a given item already in the set
        Parameters
        ----------
        i : any hashable type
            The item of the set below which the new item is inserted
        k : any hashable type
            The item to insert
        """
        if k in self._map:
            raise KeyError('Item %s already in the set' % str(k))
        if i not in self._map:
            raise KeyError('Item %s not in the set' % str(i))
        n = self._map[i]
        if n.down is None:  # Insert on top
            return self.append_bottom(k)
        # Now I know I am inserting between two actual elements
        m = self._Node(k, up=n, down=n.down)
        n.down.up = m
        n.down = m
        self._map[k] = m

    def index(self, k):
        """Return index of a given element.
        This operation has a O(n) time complexity, with n being the size of the
        set.
        Parameters
        ----------
        k : any hashable type
            The item whose index is queried
        Returns
        -------
        index : int
            The index of the item
        """
        if k not in self._map:
            raise KeyError('The item %s is not in the set' % str(k))
        index = 0
        curr = self._top
        while curr:
            if curr.val == k:
                return index
            curr = curr.down
            index += 1
        else:
            raise KeyError('It seems that the item %s is not in the set, '
                           'but you should never see this message. '
                           'There is something wrong with the code. '
                           'Debug it or report it to the developers' % str(k))

    def remove(self, k):
        """Remove an item from the set
        Parameters
        ----------
        k : any hashable type
            The item to remove
        """
        if k not in self._map:
            raise KeyError('Item %s not in the set' % str(k))
        n = self._map[k]
        if self._bottom == n:  # I am trying to remove the last node
            self._bottom = n.up
        else:
            n.down.up = n.up
        if self._top == n:  # I am trying to remove the top node
            self._top = n.down
        else:
            n.up.down = n.down
        self._map.pop(k)

    def clear(self):
        """Empty the set"""
        self._top = None
        self._bottom = None
        self._map.clear()


class Cache(object):
    """Base implementation of a cache object"""

    @abc.abstractmethod
    def __init__(self, maxlen, *args, **kwargs):
        """Constructor
        Parameters
        ----------
        maxlen : int
            The maximum number of items the cache can store
        """
        raise NotImplementedError('This method is not implemented')

    @abc.abstractmethod
    def __len__(self):
        """Return the number of items currently stored in the cache
        Returns
        -------
        len : int
            The number of items currently in the cache
        """
        raise NotImplementedError('This method is not implemented')

    @property
    @abc.abstractmethod
    def maxlen(self):
        """Return the maximum number of items the cache can store
        Return
        ------
        maxlen : int
            The maximum number of items the cache can store
        """
        raise NotImplementedError('This method is not implemented')

    @abc.abstractmethod
    def dump(self):
        """Return a dump of all the elements currently in the cache possibly
        sorted according to the eviction policy.
        Returns
        -------
        cache_dump : list
            The list of all items currently stored in the cache
        """
        raise NotImplementedError('This method is not implemented')

    def do(self, op, k, *args, **kwargs):
        """Utility method that performs a specified operation on a given item.
        This method allows to perform one of the different operations on an
        item:
         * GET: Retrieve an item
         * PUT: Insert an item
         * UPDATE: Update the value associated to an item
         * DELETE: Remove an item
        Parameters
        ----------
        op : string
            The operation to execute: GET | PUT | UPDATE | DELETE
        k : any hashable type
            The item looked up in the cache
        Returns
        -------
        res : bool
            Boolean value being *True* if the operation succeeded or *False*
            otherwise.
        """
        res = {
            'GET':    self.get,
            'PUT':    self.put,
            'UPDATE': self.put,
            'DELETE': self.remove
                }[op](k, *args, **kwargs)
        return res if res is not None else False

    @abc.abstractmethod
    def has(self, k, *args, **kwargs):
        """Check if an item is in the cache without changing the internal
        state of the caching object.
        Parameters
        ----------
        k : any hashable type
            The item looked up in the cache
        Returns
        -------
        v : bool
            Boolean value being *True* if the requested item is in the cache
            or *False* otherwise
        """
        raise NotImplementedError('This method is not implemented')

    @abc.abstractmethod
    def get(self, k, *args, **kwargs):
        """Retrieves an item from the cache.
        Differently from *has(k)*, calling this method may change the internal
        state of the caching object depending on the specific cache
        implementation.
        Parameters
        ----------
        k : any hashable type
            The item looked up in the cache
        Returns
        -------
        v : bool
            Boolean value being *True* if the requested item is in the cache
            or *False* otherwise
        """
        raise NotImplementedError('This method is not implemented')

    @abc.abstractmethod
    def put(self, k, *args, **kwargs):
        """Insert an item in the cache if not already inserted.
        If the element is already present in the cache, it will not be inserted
        again but the internal state of the cache object may change.
        Parameters
        ----------
        k : any hashable type
            The item to be inserted
        Returns
        -------
        evicted : any hashable type
            The evicted object or *None* if no contents were evicted.
        """
        raise NotImplementedError('This method is not implemented')

    @abc.abstractmethod
    def remove(self, k, *args, **kwargs):
        """Remove an item from the cache, if present.
        Parameters
        ----------
        k : any hashable type
            The item to be inserted
        Returns
        -------
        removed : bool
            *True* if the content was in the cache, *False* if it was not.
        """
        raise NotImplementedError('This method is not implemented')

    @abc.abstractmethod
    def clear(self):
        """Empty the cache
        """
        raise NotImplementedError('This method is not implemented')



@register_cache_policy('LRU')
class LruCache(Cache):
    """Least Recently Used (LRU) cache eviction policy.
    According to this policy, When a new item needs to inserted into the cache,
    it evicts the least recently requested one.
    This eviction policy is efficient for line speed operations because both
    search and replacement tasks can be performed in constant time (*O(1)*).
    This policy has been shown to perform well in the presence of temporal
    locality in the request pattern. However, its performance drops under the
    Independent Reference Model (IRM) assumption (i.e. the probability that an
    item is requested is not dependent on previous requests).
    """

    @inheritdoc(Cache)
    def __init__(self, maxlen, **kwargs):
        self._cache = LinkedSet()
        self._maxlen = int(maxlen)
        if self._maxlen <= 0:
            raise ValueError('maxlen must be positive')

    @inheritdoc(Cache)
    def __len__(self):
        return len(self._cache)

    @property
    @inheritdoc(Cache)
    def maxlen(self):
        return self._maxlen

    @inheritdoc(Cache)
    def dump(self):
        return list(iter(self._cache))

    def position(self, k, *args, **kwargs):
        """Return the current position of an item in the cache. Position *0*
        refers to the head of cache (i.e. most recently used item), while
        position *maxlen - 1* refers to the tail of the cache (i.e. the least
        recently used item).
        This method does not change the internal state of the cache.
        Parameters
        ----------
        k : any hashable type
            The item looked up in the cache
        Returns
        -------
        position : int
            The current position of the item in the cache
        """
        if k not in self._cache:
            raise ValueError('The item %s is not in the cache' % str(k))
        return self._cache.index(k)

    @inheritdoc(Cache)
    def has(self, k, *args, **kwargs):
        return k in self._cache

    @inheritdoc(Cache)
    def get(self, k, *args, **kwargs):
        # search content over the list
        # if it has it push on top, otherwise return false
        if k not in self._cache:
            return False
        self._cache.move_to_top(k)
        return True

    def put(self, k, *args, **kwargs):
        """Insert an item in the cache if not already inserted.
        If the element is already present in the cache, it will pushed to the
        top of the cache.
        Parameters
        ----------
        k : any hashable type
            The item to be inserted
        Returns
        -------
        evicted : any hashable type
            The evicted object or *None* if no contents were evicted.
        """
        # if content in cache, push it on top, no eviction
        if k in self._cache:
            self._cache.move_to_top(k)
            return None
        # if content not in cache append it on top
        self._cache.append_top(k)
        return self._cache.pop_bottom() if len(self._cache) > self._maxlen else None

    @inheritdoc(Cache)
    def remove(self, k, *args, **kwargs):
        if k not in self._cache:
            return False
        self._cache.remove(k)
        return True

    @inheritdoc(Cache)
    def clear(self):
        self._cache.clear()


@register_cache_policy('SLRU')
class SegmentedLruCache(Cache):
    """Segmented Least Recently Used (LRU) cache eviction policy.
    This policy divides the cache space into a number of segments of equal
    size each operating according to an LRU policy. When a new item is inserted
    to the cache, it is placed on the top entry of the bottom segment. Each
    subsequent hit promotes the item to the top entry of the segment above.
    When an item is evicted from a segment, it is demoted to the top entry of
    the segment immediately below. An item is evicted from the cache when it is
    evicted from the bottom segment.
    This policy can be viewed as a sort of combination between an LRU and LFU
    replacement policies as it makes eviction decisions based both frequency
    and recency of item reference.
    """

    def __init__(self, maxlen, segments=2, alloc=None, *args, **kwargs):
        """Constructor
        Parameters
        ----------
        maxlen : int
            The maximum number of items the cache can store
        segments : int
            The number of segments
        alloc : list
            List of floats, summing to 1. Indicates the fraction of overall
            caching space to be allocated to each segment.
        """
        self._maxlen = int(maxlen)
        if self._maxlen <= 0:
            raise ValueError('maxlen must be positive')
        if not isinstance(segments, int) or segments <= 0 or segments > maxlen:
            raise ValueError('segments must be an integer and 0 < segments <= maxlen')
        if alloc:
            if len(alloc) != segments:
                raise ValueError('alloc must be an iterable with as many entries as segments')
            if np.abs(np.sum(alloc) - 1) > 0.001:
                raise ValueError('All alloc entries must sum up to 1')
        else:
            alloc = [1 / segments for _ in range(segments)]
        self._segment_maxlen = apportionment(maxlen, alloc)
        self._segment = [LinkedSet() for _ in range(segments)]
        # This map is a dictionary mapping each item in the cache with the
        # segment in which it is located. This is not strictly necessary to
        # locate an item as we could have used the map in each segment.
        # This design choice however speeds up processing at the cost of a
        # moderate increase in memory footprint.
        self._cache = {}

    @inheritdoc(Cache)
    def __len__(self):
        return len(self._cache)

    @property
    @inheritdoc(Cache)
    def maxlen(self):
        return self._maxlen

    @inheritdoc(Cache)
    def has(self, k, *args, **kwargs):
        return k in self._cache

    @inheritdoc(Cache)
    def get(self, k, *args, **kwargs):
        if k not in self._cache:
            return False
        seg = self._cache[k]
        if seg == 0:
            self._segment[seg].move_to_top(k)
        else:
            self._segment[seg].remove(k)
            self._segment[seg - 1].append_top(k)
            self._cache[k] = seg - 1
            if len(self._segment[seg - 1]) > self._segment_maxlen[seg - 1]:
                demoted = self._segment[seg - 1].pop_bottom()
                self._segment[seg].append_top(demoted)
                self._cache[demoted] = seg
        return True

    def put(self, k, *args, **kwargs):
        """Insert an item in the cache if not already inserted.
        If the element is already present in the cache, it will pushed to the
        top of the cache.
        Parameters
        ----------
        k : any hashable type
            The item to be inserted
        Returns
        -------
        evicted : any hashable type
            The evicted object or *None* if no contents were evicted.
        """
        # if content in cache, promote it, no eviction
        if k in self._cache:
            seg = self._cache[k]
            if seg == 0:
                self._segment[seg].move_to_top(k)
            else:
                self._segment[seg].remove(k)
                self._segment[seg - 1].append_top(k)
                self._cache[k] = seg - 1
                if len(self._segment[seg - 1]) > self._segment_maxlen[seg - 1]:
                    demoted = self._segment[seg - 1].pop_bottom()
                    self._segment[seg].append_top(demoted)
                    self._cache[demoted] = seg
            return None
        # if content not in cache append on top of probatory segment and
        # possibly evict LRU item
        self._segment[-1].append_top(k)
        self._cache[k] = len(self._segment) - 1
        if len(self._segment[-1]) > self._segment_maxlen[-1]:
            evicted = self._segment[-1].pop_bottom()
            self._cache.pop(evicted)
            return evicted

    @inheritdoc(Cache)
    def remove(self, k, *args, **kwargs):
        if k not in self._cache:
            return False
        seg = self._cache.pop(k)
        self._segment[seg].remove(k)
        return True

    def position(self, k, *args, **kwargs):
        """Return the current position of an item in the cache. Position *0*
        refers to the head of cache (i.e. most recently used item), while
        position *maxlen - 1* refers to the tail of the cache (i.e. the least
        recently used item).
        This method does not change the internal state of the cache.
        Parameters
        ----------
        k : any hashable type
            The item looked up in the cache
        Returns
        -------
        position : int
            The current position of the item in the cache
        """
        if k not in self._cache:
            raise ValueError('The item %s is not in the cache' % str(k))
        seg = self._cache[k]
        position = self._segment[seg].index(k)
        return sum(len(self._segment[i]) for i in range(seg)) + position

    @inheritdoc(Cache)
    def dump(self, serialized=True):
        dump = list(list(iter(s)) for s in self._segment)
        return sum(dump, []) if serialized else dump

    @inheritdoc(Cache)
    def clear(self):
        self._cache.clear()
        for s in self._segment:
            s.clear()


@register_cache_policy('IN_CACHE_LFU')
class InCacheLfuCache(Cache):
    """In-cache Least Frequently Used (LFU) cache implementation
    The LFU replacement policy keeps a counter associated each item. Such
    counters are increased when the associated item is requested. Upon
    insertion of a new item, the cache evicts the one which was requested the
    least times in the past, i.e. the one whose associated value has the
    smallest value.
    This is an implementation of an In-Cache-LFU, i.e. a cache that keeps
    counters for items only as long as they are in cache and resets the
    counter of an item when it is evicted. This is different from a Perfect-LFU
    policy in which a counter is maintained also when the content is evicted.
    In-cache LFU performs better than LRU under IRM demands.
    However, its implementation is computationally expensive since it
    cannot be implemented in such a way that both search and replacement tasks
    can be executed in constant time. This makes it particularly unfit for
    large caches and line speed operations.
    """

    @inheritdoc(Cache)
    def __init__(self, maxlen, *args, **kwargs):
        self._cache = {}
        self.t = 0
        self._maxlen = int(maxlen)
        if self._maxlen <= 0:
            raise ValueError('maxlen must be positive')

    @inheritdoc(Cache)
    def __len__(self):
        return len(self._cache)

    @property
    @inheritdoc(Cache)
    def maxlen(self):
        return self._maxlen

    @inheritdoc(Cache)
    def dump(self):
        return sorted(self._cache, key=lambda x: self._cache[x], reverse=True)

    @inheritdoc(Cache)
    def has(self, k, *args, **kwargs):
        return k in self._cache

    @inheritdoc(Cache)
    def get(self, k, *args, **kwargs):
        if self.has(k):
            freq, t = self._cache[k]
            self._cache[k] = freq + 1, t
            return True
        else:
            return False

    @inheritdoc(Cache)
    def put(self, k, *args, **kwargs):
        if not self.has(k):
            self.t += 1
            self._cache[k] = (1, self.t)
            if len(self._cache) > self._maxlen:
                evicted = min(self._cache, key=lambda x: self._cache[x])
                self._cache.pop(evicted)
                return evicted
        return None

    @inheritdoc(Cache)
    def remove(self, k, *args, **kwargs):
        if k in self._cache:
            self._cache.pop(k)
            return True
        else:
            return False

    @inheritdoc(Cache)
    def clear(self):
        self._cache.clear()


@register_cache_policy('PERFECT_LFU')
class PerfectLfuCache(Cache):
    """Perfect Least Frequently Used (LFU) cache implementation
    The LFU replacement policy keeps a counter associated each item. Such
    counters are increased when the associated item is requested. Upon
    insertion of a new item, the cache evicts the one which was requested the
    least times in the past, i.e. the one whose associated value has the
    smallest value.
    This is an implementation of a Perfect-LFU, i.e. a cache that keeps
    counters for every item, even for those not in the cache.
    In contrast to LRU, Perfect-LFU has been shown to perform optimally under
    IRM demands. However, its implementation is computationally expensive since
    it cannot be implemented in such a way that both search and replacement
    tasks can be executed in constant time. This makes it particularly unfit
    for large caches and line speed operations.
    """

    @inheritdoc(Cache)
    def __init__(self, maxlen, *args, **kwargs):
        # Dict storing counter for all contents, not only those in cache
        self._counter = {}
        # Set storing only items currently in cache
        self._cache = set()
        self.t = 0
        self._maxlen = int(maxlen)
        if self._maxlen <= 0:
            raise ValueError('maxlen must be positive')

    @inheritdoc(Cache)
    def __len__(self):
        return len(self._cache)

    @property
    @inheritdoc(Cache)
    def maxlen(self):
        return self._maxlen

    @inheritdoc(Cache)
    def dump(self):
        return sorted(self._cache, key=lambda x: self._counter[x], reverse=True)

    @inheritdoc(Cache)
    def has(self, k, *args, **kwargs):
        return k in self._cache

    @inheritdoc(Cache)
    def get(self, k, *args, **kwargs):
        self.t += 1
        if k in self._counter:
            freq, t = self._counter[k]
            self._counter[k] = freq + 1, t
        else:
            self._counter[k] = 1, self.t
        if self.has(k):
            return True
        else:
            return False

    @inheritdoc(Cache)
    def put(self, k, *args, **kwargs):
        if not self.has(k):
            if k in self._counter:
                freq, t = self._counter[k]
                self._counter[k] = (freq + 1, t)
            else:
                # If I always call a get before a put, this line should never
                # be executed
                self._counter[k] = (1, self.t)
            self._cache.add(k)
            if len(self._cache) > self._maxlen:
                evicted = min(self._cache, key=lambda x: self._counter[x])
                self._cache.remove(evicted)
                return evicted
        return None

    @inheritdoc(Cache)
    def remove(self, k, *args, **kwargs):
        if k in self._cache:
            self._cache.pop(k)
            return True
        else:
            return False

    @inheritdoc(Cache)
    def clear(self):
        self._cache.clear()
        self._counter.clear()


@register_cache_policy('FIFO')
class FifoCache(Cache):
    """First In First Out (FIFO) cache implementation.
    According to the FIFO policy, when a new item is inserted, the evicted item
    is the first one inserted in the cache. The behavior of this policy differs
    from LRU only when an item already present in the cache is requested.
    In fact, while in LRU this item would be pushed to the top of the cache, in
    FIFO no movement is performed. The FIFO policy has a slightly simpler
    implementation in comparison to the LRU policy but yields worse performance.
    """

    @inheritdoc(Cache)
    def __init__(self, maxlen, *args, **kwargs):
        self._cache = set()
        self._maxlen = int(maxlen)
        self._d = deque()
        if self._maxlen <= 0:
            raise ValueError('maxlen must be positive')

    @inheritdoc(Cache)
    def __len__(self):
        return len(self._cache)

    @property
    @inheritdoc(Cache)
    def maxlen(self):
        return self._maxlen

    @inheritdoc(Cache)
    def dump(self):
        return list(self._d)

    @inheritdoc(Cache)
    def has(self, k, *args, **kwargs):
        return k in self._cache

    def position(self, k, *args, **kwargs):
        """Return the current position of an item in the cache. Position *0*
        refers to the head of cache (i.e. most recently inserted item), while
        position *maxlen - 1* refers to the tail of the cache (i.e. the least
        recently inserted item).
        This method does not change the internal state of the cache.
        Parameters
        ----------
        k : any hashable type
            The item looked up in the cache
        Returns
        -------
        position : int
            The current position of the item in the cache
        """
        i = 0
        for c in self._d:
            if c == k:
                return i
            i += 1
        raise ValueError('The item %s is not in the cache' % str(k))

    @inheritdoc(Cache)
    def get(self, k, *args, **kwargs):
        return self.has(k)

    @inheritdoc(Cache)
    def put(self, k, *args, **kwargs):
        evicted = None
        if not self.has(k):
            self._cache.add(k)
            self._d.appendleft(k)
        if len(self._cache) > self.maxlen:
            evicted = self._d.pop()
            self._cache.remove(evicted)
        return evicted

    @inheritdoc(Cache)
    def remove(self, k, *args, **kwargs):
        if k in self._cache:
            self._cache.remove(k)
            self._d.remove(k)
            return True
        else:
            return False

    @inheritdoc(Cache)
    def clear(self):
        self._cache.clear()
        self._d.clear()