r"""
LeetCode 146 - LRU Cache
-------------------------
Design a data structure that follows the Least Recently Used (LRU) cache rule.

  LRUCache(capacity)  -> create the cache with a positive size
  get(key)            -> return the value if the key exists, else -1
  put(key, value)     -> insert or update the key. If the number of keys goes
                         over capacity, evict the LEAST recently used key.

Both get() and put() must run in O(1) average time.

Example:
    cache = LRUCache(2)
    cache.put(1, 1)      # cache: {1=1}
    cache.put(2, 2)      # cache: {1=1, 2=2}
    cache.get(1)         # returns 1, order is now 2 (oldest), 1 (newest)
    cache.put(3, 3)      # full, evicts key 2 -> cache: {1=1, 3=3}
    cache.get(2)         # returns -1 (evicted)
    cache.put(4, 4)      # full, evicts key 1 -> cache: {3=3, 4=4}
    cache.get(1)         # returns -1 (evicted)
    cache.get(3)         # returns 3
    cache.get(4)         # returns 4

The key point: BOTH get and put count as "using" a key. Reading a key makes it
the most recently used one, so it must be protected from eviction. We need
  (a) O(1) lookup by key            -> a hash map
  (b) O(1) "move to most recent"    -> an ordered structure that can remove
      and re-add an item in O(1)       from the middle
  (c) O(1) "evict the oldest"       -> access to the oldest end of that order

Four approaches are given below.

Summary
-------
 #  Approach                                  get     put     Space   Notes
 1  Dict + list of keys (brute force)         O(n)    O(n)    O(c)    Simple, but list.remove is linear. Fails the O(1) rule
 2  OrderedDict (RECOMMENDED for practice)    O(1)    O(1)    O(c)    Your version, shortest, uses built-in ordering
 3  Plain dict (insertion order)              O(1)    O(1)    O(c)    Python 3.7+ dicts keep insertion order, no import
 4  Hash map + doubly linked list             O(1)    O(1)    O(c)    What interviewers usually expect, you build it by hand

 (c = capacity, the maximum number of keys stored)
"""

from collections import OrderedDict


class LRUCacheNaive:
    """
    Approach 1: Dict + list of keys (brute force)
    -----------------------------------------------
    Idea:
      - Keep a dict for key -> value, and a list that stores the keys from
        least recently used (front) to most recently used (back).
      - On get or put of an existing key, remove the key from the list and
        append it to the back.
      - When the cache is full and a new key arrives, pop the front of the
        list (the least recently used) and delete it from the dict.

    Walkthrough with capacity = 2:
        put(1, 1): order = [1]
        put(2, 2): order = [1, 2]
        get(1):    order = [2, 1]      (1 moved to the back)
        put(3, 3): full, evict order[0] = 2 -> order = [1, 3]

    Time Complexity:  O(n) per operation -- list.remove(key) scans the list
                      and pop(0) shifts every element.
    Space Complexity: O(c) -- dict and list each hold at most c keys.

    Things to be aware of:
      - Good as a first correct answer to explain the logic, then improve it.
      - Does NOT meet the O(1) requirement, so large inputs time out.

    Common pitfalls:
      - Forgetting to refresh the order when get() hits a key.
      - Evicting when updating an existing key. Updating never adds a new
        key, so the size does not grow and nothing should be evicted.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data = {}
        self.order = []  # least recent at index 0, most recent at the end

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        if key in self.data:
            self.order.remove(key)
        elif len(self.data) >= self.capacity:
            oldest = self.order.pop(0)
            del self.data[oldest]
        self.data[key] = value
        self.order.append(key)


class LRUCacheOrderedDict:
    """
    Approach 2 (RECOMMENDED for practice): OrderedDict
    ----------------------------------------------------
    Idea:
      - OrderedDict remembers the order keys were inserted and supports
        moving a key to either end in O(1).
      - Keep the order as: first item = least recently used, last item =
        most recently used.
      - get: if the key exists, move_to_end(key) and return its value.
      - put: if the key exists, move_to_end(key). Otherwise, if the cache is
        full, popitem(last=False) removes the first (oldest) item. Then
        store the value.

    Walkthrough with capacity = 2:
        put(1, 1): {1}
        put(2, 2): {1, 2}
        get(1):    move 1 to the end -> {2, 1}, returns 1
        put(3, 3): full, popitem(last=False) removes 2 -> {1, 3}
        get(2):    not found -> -1

    Time Complexity:  O(1) -- hash lookup, move_to_end and popitem are all
                      constant time.
    Space Complexity: O(c) -- at most c keys are stored.

    Things to be aware of:
      - Shortest correct solution, and the one to use in real code.
      - Interviewers may say "do not use OrderedDict" because it hides the
        real work. Approach 4 is the answer for that case.
      - The eviction check runs only for a NEW key. For an existing key the
        size does not change, so we only refresh its position.

    Common pitfalls:
      - popitem() with no argument removes the LAST item (most recent).
        Use popitem(last=False) to remove the oldest.
      - Assigning self.cache[key] = value without move_to_end for an existing
        key. Assigning to an existing key does not change its position.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        elif self.capacity <= len(self.cache):
            self.cache.popitem(last=False)
        self.cache[key] = value


class LRUCacheDict:
    """
    Approach 3: Plain dict (relies on insertion order)
    ----------------------------------------------------
    Idea:
      - Since Python 3.7 a normal dict keeps keys in insertion order.
      - To mark a key as "most recently used", delete it and insert it again.
        Re-inserting puts it at the end.
      - The least recently used key is always the first key in the dict,
        which we get with next(iter(d)).

    Walkthrough with capacity = 2:
        put(1, 1): {1}
        put(2, 2): {1, 2}
        get(1):    pop 1, insert again -> {2, 1}
        put(3, 3): full, first key is 2, delete it -> {1, 3}

    Time Complexity:  O(1) average -- pop, insert and next(iter(d)) are
                      constant time on average.
    Space Complexity: O(c) -- at most c keys are stored.

    Things to be aware of:
      - No import needed, but it depends on Python 3.7+ ordering behavior.
      - next(iter(d)) is O(1) in practice. In a dict with many deleted
        entries at the front it can slow down a little, because the dict
        skips over the empty slots. Fine for LeetCode, but OrderedDict is
        safer for heavy workloads.

    Common pitfalls:
      - Evicting before checking if the key already exists. Updating an
        existing key must not evict anything.
      - Reading the value without re-inserting the key, so the key keeps
        its old (stale) position.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        self.cache[key] = value


class _Node:
    """A node of the doubly linked list, stores the key so we can evict it."""

    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    """
    Approach 4: Hash map + Doubly linked list (build it by hand)
    --------------------------------------------------------------
    Idea:
      - This is what OrderedDict does inside. Two pieces work together:
          * a hash map: key -> node, for O(1) lookup
          * a doubly linked list of nodes ordered by recent use, so a node can
            be unlinked and relinked in O(1) because it knows prev and next
      - Use two dummy nodes, `head` and `tail`, so there are no special cases
        for an empty list or for the first and last real node.
            head <-> (least recent) ... (most recent) <-> tail
      - Least recent node is always head.next. Most recent is tail.prev.
      - get: find the node in the map, move it just before tail, return val.
      - put: if the key exists, update val and move the node to the end.
        Otherwise create a node, add it before tail, and if the size is now
        over capacity remove head.next and delete its key from the map.

    Walkthrough with capacity = 2:
        put(1, 1): head <-> 1 <-> tail
        put(2, 2): head <-> 1 <-> 2 <-> tail
        get(1):    unlink 1, add before tail -> head <-> 2 <-> 1 <-> tail
        put(3, 3): add 3 -> head <-> 2 <-> 1 <-> 3 <-> tail, size 3 > 2,
                   remove head.next (2), delete key 2 from the map
                   -> head <-> 1 <-> 3 <-> tail

    Time Complexity:  O(1) -- map lookup plus a fixed number of pointer
                      changes per operation.
    Space Complexity: O(c) -- one node and one map entry per stored key.

    Things to be aware of:
      - The node stores its own key. Without it, when we evict head.next we
        would not know which map entry to delete.
      - Dummy head and tail mean _remove and _add never check for None.
      - Order of pointer updates matters in _add. Set the new node's
        pointers first, then rewire the neighbours.

    Common pitfalls:
      - Forgetting to delete the evicted key from the map (stale entry that
        points to a node no longer in the list).
      - Updating an existing key but not moving it to the most recent end.
      - Evicting when the size is exactly equal to capacity instead of
        greater than it (off by one), or evicting before inserting the new
        node without checking the key already exists.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_end(self, node: _Node) -> None:
        # insert node just before tail (most recent position)
        last = self.tail.prev
        node.prev = last
        node.next = self.tail
        last.next = node
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_to_end(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_to_end(node)
            return

        node = _Node(key, value)
        self.map[key] = node
        self._add_to_end(node)

        if len(self.map) > self.capacity:
            oldest = self.head.next
            self._remove(oldest)
            del self.map[oldest.key]


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)


if __name__ == "__main__":
    # Quick self-check: run the problem's example on every approach.
    for impl in (LRUCacheNaive, LRUCacheOrderedDict, LRUCacheDict, LRUCache):
        c = impl(2)
        c.put(1, 1)
        c.put(2, 2)
        assert c.get(1) == 1
        c.put(3, 3)
        assert c.get(2) == -1
        c.put(4, 4)
        assert c.get(1) == -1
        assert c.get(3) == 3
        assert c.get(4) == 4

        # updating an existing key must not evict anything
        d = impl(2)
        d.put(1, 1)
        d.put(2, 2)
        d.put(2, 20)
        assert d.get(1) == 1 and d.get(2) == 20
        print(impl.__name__, "OK")