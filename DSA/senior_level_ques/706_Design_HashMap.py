r"""
LeetCode 706 - Design HashMap
-------------------------------
Design a hash map WITHOUT using any built-in hash table library (no dict).

  MyHashMap()            -> create an empty map
  put(key, value)        -> insert the pair, or update the value if the key
                            already exists
  get(key)               -> return the value for the key, or -1 if missing
  remove(key)            -> delete the key and its value if it exists

Constraints: 0 <= key, value <= 10^6, at most 10^4 calls in total.

Example:
    m = MyHashMap()
    m.put(1, 1)          # map: {1=1}
    m.put(2, 2)          # map: {1=1, 2=2}
    m.get(1)             # returns 1
    m.get(3)             # returns -1 (missing)
    m.put(2, 1)          # key 2 exists, value updated -> {1=1, 2=1}
    m.get(2)             # returns 1
    m.remove(2)          # map: {1=1}
    m.get(2)             # returns -1

The key point: a hash function turns a key into an array index, but two
different keys can land on the same index (a COLLISION). Every approach below
is really a different answer to "what do we do on a collision, and how do we
keep collisions rare?"

Four approaches are given below.

Summary
-------
 #  Approach                                   Avg time    Worst     Space     Notes
 1  Direct address table                       O(1)        O(1)      O(K)      No collisions at all, but wastes memory (K = key range, 10^6)
 2  Fixed buckets + chaining                   O(n/B)      O(n)      O(B + n)  Your first version, simple, slows down as n grows
 3  Chaining + dynamic resizing (RECOMMENDED)  O(1) amort. O(n)      O(n)      Your second version, how real hash tables behave
 4  Open addressing (linear probing)           O(1) amort. O(n)      O(n)      No lists, uses tombstones for deletion

 (n = number of stored keys, B = number of buckets, K = size of the key range)
"""


class MyHashMapDirect:
    """
    Approach 1: Direct address table
    ----------------------------------
    Idea:
      - Keys are guaranteed to be in 0..10^6, so use the key itself as the
        array index. No hash function, no collisions.
      - Store -1 in a slot to mean "no value". Values are never negative, so
        -1 is safe as a marker.
      - put: data[key] = value
      - get: return data[key] (already -1 when missing)
      - remove: data[key] = -1

    Walkthrough:
        put(2, 2):  data[2] = 2
        put(2, 1):  data[2] = 1          (update is the same as insert)
        get(3):     data[3] is -1 -> -1
        remove(2):  data[2] = -1

    Time Complexity:  O(1) for every operation, worst case too.
    Space Complexity: O(K) -- one slot for every possible key, here about
                      10^6 slots no matter how few keys are stored.

    Things to be aware of:
      - Fastest and simplest, and fine for this problem's limits.
      - It only works because the key range is small and known. For
        arbitrary keys (strings, large ints) it cannot be used.
      - It does not show hashing at all, so interviewers usually want one of
        the approaches below.

    Common pitfalls:
      - Using 0 as the "empty" marker. 0 is a valid value, so use -1.
      - Making the array 10^6 long instead of 10^6 + 1. Key 10^6 would be
        out of range.
    """

    def __init__(self):
        self.data = [-1] * (10**6 + 1)

    def put(self, key: int, value: int) -> None:
        self.data[key] = value

    def get(self, key: int) -> int:
        return self.data[key]

    def remove(self, key: int) -> None:
        self.data[key] = -1


class MyHashMapFixed:
    """
    Approach 2: Fixed number of buckets + chaining
    ------------------------------------------------
    Idea:
      - Keep an array of B buckets. Each bucket is a list of (key, value)
        pairs. This is called separate chaining.
      - The hash function picks the bucket: index = hash(key) % B.
      - put: look through the bucket. If the key is there, replace the pair.
        Otherwise append a new pair.
      - get: look through the bucket for the key, return its value or -1.
      - remove: find the pair in the bucket and delete it.

    Walkthrough with B = 4:
        put(1, 10): 1 % 4 = 1 -> bucket 1: [(1, 10)]
        put(5, 50): 5 % 4 = 1 -> bucket 1: [(1, 10), (5, 50)]   collision
        get(5):     bucket 1, skip (1, 10), match (5, 50) -> 50
        remove(1):  bucket 1: [(5, 50)]

    Time Complexity:  O(n / B) on average -- each bucket holds about n / B
                      pairs. Worst case O(n) if every key lands in one
                      bucket.
    Space Complexity: O(B + n) -- B bucket lists plus the n stored pairs.

    Things to be aware of:
      - B never changes, so as n grows the buckets get longer and every
        operation slows down. With B = 100 and a million keys, each bucket
        holds about 10,000 pairs.
      - A prime B (769 is a common choice) spreads keys more evenly than a
        round number like 100 when keys follow a pattern.
      - Python's hash(int) returns the int itself, and `%` always gives a
        non-negative result, so the index is always valid.
      - The original code had a leftover print(key) in remove. It is removed
        here, since extra output can break judging.

    Common pitfalls:
      - Appending without checking for an existing key, which creates
        duplicate keys in the bucket.
      - Calling bucket.remove(...) or pop(...) and then continuing the loop.
        Returning right after the change avoids skipping elements.
    """

    def __init__(self):
        self.size = 769
        self.buckets = [[] for _ in range(self.size)]

    def _index(self, key: int) -> int:
        return hash(key) % self.size

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key: int) -> int:
        for k, v in self.buckets[self._index(key)]:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return


class MyHashMap:
    """
    Approach 3 (RECOMMENDED): Chaining with dynamic resizing
    ----------------------------------------------------------
    Idea:
      - Same bucket-of-lists design as Approach 2, but the number of
        buckets grows with the data so the chains stay short.
      - Track `count`, the number of stored keys. The load factor is
        count / capacity, the average chain length.
      - After inserting a NEW key, if the load factor reaches 0.75, double
        the capacity and rehash every pair into the new bucket array.
      - Updates of an existing key do not change count, so they never
        trigger a resize.

    Walkthrough with capacity = 4, threshold 0.75:
        put(1, 1): count 1, load 0.25
        put(2, 2): count 2, load 0.50
        put(3, 3): count 3, load 0.75 -> resize to capacity 8
                   every key is rehashed: index = key % 8
        put(2, 9): key exists, value updated, count stays 3

    Time Complexity:  O(1) amortized for put, get and remove. A single
                      resize costs O(n), but doubling means it happens
                      rarely, so the cost spread over all puts is O(1).
                      Worst case O(n) if all keys collide.
    Space Complexity: O(n) -- capacity stays within a constant factor of
                      the number of keys.

    Things to be aware of:
      - Rehashing is required. The index depends on capacity, so after the
        capacity changes, old positions are wrong. You cannot just copy the
        buckets over.
      - This is how real hash tables work (Java HashMap uses the same 0.75
        load factor).
      - remove decrements count, but the table never shrinks. That is fine
        here, but a production version might shrink at a low load factor.

    Common pitfalls:
      - Incrementing count when an existing key is updated. That makes the
        load factor look higher than it is and triggers needless resizes.
      - Forgetting to decrement count in remove.
      - Rehashing with the OLD capacity. Double the capacity first, then
        compute new indexes.
    """

    def __init__(self):
        self.capacity = 4
        self.count = 0
        self.load_factor = 0.75
        self.buckets = [[] for _ in range(self.capacity)]

    def _index(self, key: int) -> int:
        return hash(key) % self.capacity

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[self._index(key)]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.count += 1

        if self.count / self.capacity >= self.load_factor:
            self._resize()

    def get(self, key: int) -> int:
        for k, v in self.buckets[self._index(key)]:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.count -= 1
                return

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]

        for bucket in old_buckets:
            for key, value in bucket:
                self.buckets[self._index(key)].append((key, value))


class MyHashMapOpenAddressing:
    """
    Approach 4: Open addressing (linear probing) with tombstones
    --------------------------------------------------------------
    Idea:
      - No lists. Every key and value lives directly in one flat array.
      - On a collision, step forward one slot at a time (index + 1, wrapping
        around) until a usable slot is found. This is linear probing.
      - Each slot has a state: EMPTY (never used), USED, or DELETED (a
        tombstone left behind by remove).
      - get: probe from the hash index. Stop and return -1 at the first
        EMPTY slot. Skip DELETED slots and keep going.
      - remove: find the key and mark the slot DELETED. It cannot be set back
        to EMPTY, because that would cut the probe path of other keys that
        collided past this slot.
      - put: probe for the key. If found, update it. If not found, insert
        into the first DELETED slot seen on the way, else the EMPTY slot
        where the probe ended.
      - Keep the table at most half full (counting tombstones) by doubling
        and rehashing only the live pairs, which also clears the tombstones.

    Walkthrough with capacity = 8:
        put(1, 10): 1 % 8 = 1 -> slot 1
        put(9, 90): 9 % 8 = 1 taken -> slot 2
        remove(1):  slot 1 becomes DELETED (a tombstone, not EMPTY)
        get(9):     slot 1 is DELETED, skip -> slot 2 matches -> 90
                    (if slot 1 were EMPTY, we would stop and wrongly
                    return -1)

    Time Complexity:  O(1) amortized for every operation, because the
                      table is kept at most half full so probes stay short.
                      Worst case O(n) when many keys cluster together.
    Space Complexity: O(n) -- three flat arrays of size capacity.

    Things to be aware of:
      - Good cache behavior since everything is in contiguous arrays.
      - Tombstones count toward the load, so a table with many removes and
        few live keys still needs to be rebuilt.
      - Probing needs at least one EMPTY slot to terminate. Keeping the load
        at 0.5 or below guarantees that.

    Common pitfalls:
      - Marking a removed slot EMPTY instead of DELETED, which breaks get
        for keys that probed past it.
      - Inserting into the first DELETED slot before checking the rest of the
        probe path for the same key, which creates a duplicate key.
      - Counting a reused tombstone as a new filled slot.
    """

    EMPTY, USED, DELETED = 0, 1, 2

    def __init__(self):
        self.capacity = 8
        self.live = 0       # number of USED slots
        self.filled = 0     # USED + DELETED slots, drives resizing
        self._alloc()

    def _alloc(self) -> None:
        self.state = [self.EMPTY] * self.capacity
        self.keys = [0] * self.capacity
        self.vals = [0] * self.capacity

    def _find(self, key: int) -> int:
        """Return the slot holding key, or -1 if it is not in the table."""
        idx = hash(key) % self.capacity
        for _ in range(self.capacity):
            if self.state[idx] == self.EMPTY:
                return -1
            if self.state[idx] == self.USED and self.keys[idx] == key:
                return idx
            idx = (idx + 1) % self.capacity
        return -1

    def put(self, key: int, value: int) -> None:
        found = self._find(key)
        if found != -1:
            self.vals[found] = value
            return

        idx = hash(key) % self.capacity
        first_deleted = -1
        while self.state[idx] != self.EMPTY:
            if self.state[idx] == self.DELETED and first_deleted == -1:
                first_deleted = idx
            idx = (idx + 1) % self.capacity

        if first_deleted != -1:
            idx = first_deleted      # reuse a tombstone, filled unchanged
        else:
            self.filled += 1         # consumed a brand new EMPTY slot

        self.state[idx] = self.USED
        self.keys[idx] = key
        self.vals[idx] = value
        self.live += 1

        if self.filled / self.capacity > 0.5:
            self._resize()

    def get(self, key: int) -> int:
        idx = self._find(key)
        return self.vals[idx] if idx != -1 else -1

    def remove(self, key: int) -> None:
        idx = self._find(key)
        if idx != -1:
            self.state[idx] = self.DELETED
            self.live -= 1

    def _resize(self) -> None:
        old = [(self.keys[i], self.vals[i])
               for i in range(self.capacity) if self.state[i] == self.USED]
        self.capacity *= 2
        self.live = 0
        self.filled = 0
        self._alloc()
        for k, v in old:
            self.put(k, v)


# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)


if __name__ == "__main__":
    import random

    impls = (MyHashMapDirect, MyHashMapFixed, MyHashMap, MyHashMapOpenAddressing)

    # 1) The problem's example on every approach.
    for impl in impls:
        m = impl()
        m.put(1, 1)
        m.put(2, 2)
        assert m.get(1) == 1
        assert m.get(3) == -1
        m.put(2, 1)
        assert m.get(2) == 1
        m.remove(2)
        assert m.get(2) == -1

    # 2) Random operations compared against a real dict (test only).
    random.seed(0)
    for impl in impls:
        m, ref = impl(), {}
        for _ in range(20000):
            op = random.choice(("put", "get", "remove"))
            k = random.randint(0, 300)
            if op == "put":
                v = random.randint(0, 10**6)
                m.put(k, v)
                ref[k] = v
            elif op == "get":
                assert m.get(k) == ref.get(k, -1)
            else:
                m.remove(k)
                ref.pop(k, None)
        print(impl.__name__, "OK")