from typing import List


# ─────────────────────────────────────────────────────────────
# APPROACH 1 — Sort First
# ─────────────────────────────────────────────────────────────
# Idea: Sort the array, then do a single linear scan counting
#       consecutive runs.
#
# Time  : O(n log n)  — dominated by the sort
# Space : O(1)        — sorting in-place, only scalar counters
# ─────────────────────────────────────────────────────────────
class Solution1:
    def longestConsecutive(self, nums: List[int]) -> int:
        if len(nums) == 0:
            return 0

        nums.sort()  # bring consecutive numbers next to each other

        count, max_count = 1, 1

        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1] + 1:
                # extend the current consecutive run
                count += 1
                max_count = max(max_count, count)
            elif nums[i] == nums[i - 1]:
                # duplicate — skip without resetting the run
                continue
            else:
                # gap found; restart the run counter
                count = 1

        return max_count


# ─────────────────────────────────────────────────────────────
# APPROACH 2 — Hash Set  ✦ optimal
# ─────────────────────────────────────────────────────────────
# Idea: Load all numbers into a set for O(1) look-ups.
#       Only start counting from a sequence's *first* element
#       (i.e. when num-1 is absent) to avoid redundant work.
#       Each number is visited at most twice → O(n) overall.
#
# Time  : O(n)  — set construction + each element touched ≤ 2×
# Space : O(n)  — the hash set stores all unique numbers
# ─────────────────────────────────────────────────────────────
class Solution2:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)  # O(1) average look-up
        longest = 0

        for num in num_set:
            # only begin a new sequence at its smallest element
            if num - 1 not in num_set:
                length = 1
                # walk forward as long as the next number exists
                while num + length in num_set:
                    length += 1
                longest = max(longest, length)

        return longest


# ─────────────────────────────────────────────────────────────
# APPROACH 3 — HashMap (sequence length tracking)
# ─────────────────────────────────────────────────────────────
# Idea: Use a dict that maps each number to the length of the
#       consecutive sequence it belongs to. When inserting a
#       number, check its left (num-1) and right (num+1)
#       neighbours and merge their sequences immediately.
#       The boundary elements always hold the correct length,
#       so a single pass is enough.
#
# Time  : O(n)   — one pass; each merge is O(1)
# Space : O(n)   — the dict stores every unique number
# ─────────────────────────────────────────────────────────────
class Solution3:
    def longestConsecutive(self, nums: List[int]) -> int:
        length_map: dict[int, int] = {}  # num → sequence length
        longest = 0

        for num in nums:
            if num in length_map:
                continue  # already processed this number

            left  = length_map.get(num - 1, 0)  # length of sequence ending   at num-1
            right = length_map.get(num + 1, 0)  # length of sequence starting at num+1

            total = left + 1 + right
            length_map[num] = total
            longest = max(longest, total)

            # Update the boundary elements so future merges are correct.
            # Only the far ends of the merged window need updating because
            # those are the only elements queried by future neighbours.
            length_map[num - left]  = total   # left boundary
            length_map[num + right] = total   # right boundary

        return longest


# ─────────────────────────────────────────────────────────────
# APPROACH 4 — Union-Find (Disjoint Set Union)
# ─────────────────────────────────────────────────────────────
# Idea: Treat each number as a node. Union every num with
#       num+1 if it exists. The size of the largest component
#       is the answer.  Path compression + union-by-rank keeps
#       each operation near O(1) amortised.
#
# Time  : O(n · α(n)) ≈ O(n)  — α is the inverse-Ackermann fn
# Space : O(n)                 — parent / rank / size arrays
# ─────────────────────────────────────────────────────────────
class UnionFind:
    def __init__(self, nums):
        self.parent = {n: n for n in nums}
        self.rank   = {n: 0  for n in nums}
        self.size   = {n: 1  for n in nums}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        # union by rank
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

    def max_size(self):
        return max(self.size[self.find(n)] for n in self.size)


class Solution4:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        num_set = set(nums)
        uf = UnionFind(num_set)

        for num in num_set:
            if num + 1 in num_set:
                uf.union(num, num + 1)

        return uf.max_size()


# ─────────────────────────────────────────────────────────────
# APPROACH 5 — Bucket / Pigeonhole (integer-range aware)
# ─────────────────────────────────────────────────────────────
# Idea: When the value range R = max-min+1 is not too large,
#       mark a boolean array of size R, then do one linear scan
#       exactly like the Sort approach — but in O(R) time with
#       no comparison sort needed.
#
# Best for dense inputs where R ≈ n.
#
# Time  : O(n + R)  — fill + scan; O(n) when R = O(n)
# Space : O(R)      — the boolean bucket array
# ─────────────────────────────────────────────────────────────
class Solution5:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        lo, hi = min(nums), max(nums)
        R = hi - lo + 1

        # Only worthwhile when the range is manageable
        # (falls back gracefully for sparse inputs)
        present = [False] * R
        for n in nums:
            present[n - lo] = True

        longest = count = 0
        for exists in present:
            if exists:
                count += 1
                longest = max(longest, count)
            else:
                count = 0

        return longest


# ─────────────────────────────────────────────────────────────
# Quick comparison
# ─────────────────────────────────────────────────────────────
# | Approach             | Time        | Space | Notes                          |
# |----------------------|-------------|-------|--------------------------------|
# | 1. Sort              | O(n log n)  | O(1)  | Modifies input; cache-friendly |
# | 2. Hash Set          | O(n)        | O(n)  | Clean & optimal; preferred     |
# | 3. HashMap           | O(n)        | O(n)  | Streams well; no re-traversal  |
# | 4. Union-Find        | O(n · α(n)) | O(n)  | Graph-flavoured; reusable DSU  |
# | 5. Bucket/Pigeonhole | O(n + R)    | O(R)  | Best when range R ≈ n (dense)  |
# ─────────────────────────────────────────────────────────────