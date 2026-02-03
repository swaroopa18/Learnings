"""
============================================================
LeetCode 295 — Find Median from Data Stream
============================================================

Four solutions, ranked from naive to optimal:

    1. BruteForceMedianFinder   — Sort on every query
    2. BisectMedianFinder       — Sorted insert via bisect
    3. TwoHeapMedianFinderV1    — Two heaps, manual routing
    4. TwoHeapMedianFinderV2    — Two heaps, push-then-fix  ← BEST

Complexity Summary:
┌─────────────────────────┬──────────────┬────────────────┐
│ Approach                │ addNum       │ findMedian     │
├─────────────────────────┼──────────────┼────────────────┤
│ Brute Force             │ O(1)         │ O(n log n)     │
│ Bisect Insert           │ O(n)         │ O(1)           │
│ Two Heaps v1            │ O(log n)     │ O(1)           │
│ Two Heaps v2 (Best)     │ O(log n)     │ O(1)           │
└─────────────────────────┴──────────────┴────────────────┘
Space: O(n) for all approaches.
"""

import heapq
import bisect


# ============================================================
# 1. BRUTE FORCE — Sort on Every Query
# ============================================================
# Time:  addNum → O(1)  |  findMedian → O(n log n)
# Space: O(n)
#
# How it works:
#   - Append every number into a plain list.
#   - On findMedian, sort the entire list, then return the middle.
#
# Pitfalls:
#   - Sorting on every findMedian call is redundant if no new
#     numbers were added since the last query.
#   - Only acceptable as a naive starting point.
# ============================================================
class BruteForceMedianFinder:
    def __init__(self):
        self.nums = []

    def addNum(self, num: int) -> None:
        # O(1) — just append
        self.nums.append(num)

    def findMedian(self) -> float:
        # O(n log n) — sort the whole list every time
        self.nums.sort()
        n = len(self.nums)
        mid = n // 2

        if n % 2 == 0:
            # Even count → average of the two middle elements
            return (self.nums[mid - 1] + self.nums[mid]) / 2
        else:
            # Odd count → the single middle element
            return float(self.nums[mid])


# ============================================================
# 2. BISECT — Sorted Insert
# ============================================================
# Time:  addNum → O(n)  |  findMedian → O(1)
# Space: O(n)
#
# How it works:
#   - Maintain a list that is always sorted.
#   - Use bisect.insort to insert in the correct position.
#   - findMedian just indexes into the middle — O(1).
#
# Pitfalls:
#   - bisect.insort finds the position in O(log n), but
#     list.insert shifts all following elements in O(n).
#   - Net addNum is O(n), not O(log n).
#   - Good choice when reads (findMedian) far outnumber
#     writes (addNum), or when code brevity matters.
# ============================================================
class BisectMedianFinder:
    def __init__(self):
        self.nums = []  # always kept sorted

    def addNum(self, num: int) -> None:
        # O(log n) search + O(n) shift = O(n) total
        bisect.insort(self.nums, num)

    def findMedian(self) -> float:
        # O(1) — list is already sorted, just index the middle
        n = len(self.nums)
        mid = n // 2

        if n % 2 == 0:
            return (self.nums[mid - 1] + self.nums[mid]) / 2
        return float(self.nums[mid])


# ============================================================
# 3. TWO HEAPS v1 — Manual Routing & Balancing
# ============================================================
# Time:  addNum → O(log n)  |  findMedian → O(1)
# Space: O(n)
#
# How it works:
#   - A = max heap (lower half, stored as negatives)
#   - B = min heap (upper half)
#   - Route the incoming number into A or B based on its value.
#   - Rebalance sizes so they differ by at most 1.
#
# Pitfalls:
#   - Routing assumes A is non-empty — needs the
#     `len(self.A) == 0` guard or it crashes.
#   - Routing alone does NOT guarantee max(A) <= min(B).
#     If a number lands in the wrong heap, the invariant
#     breaks silently and the median will be wrong.
#   - The early return on balanced sizes is fine, but the
#     if/elif beneath it becomes fragile if that guard is
#     ever removed or changed.
#   - v2 below fixes all of these issues.
# ============================================================
class TwoHeapMedianFinderV1:
    def __init__(self):
        self.A = []  # max heap (store negatives)
        self.B = []  # min heap

    def addNum(self, num: int) -> None:
        # Route into A (lower half) or B (upper half)
        if len(self.A) == 0 or num <= -self.A[0]:
            heapq.heappush(self.A, -num)
        else:
            heapq.heappush(self.B, num)

        # Already balanced — nothing to do
        if abs(len(self.A) - len(self.B)) <= 1:
            return

        # Rebalance: move from the larger heap to the smaller
        if len(self.A) > len(self.B) + 1:
            ele = heapq.heappop(self.A)
            heapq.heappush(self.B, -ele)       # flip sign back
        elif len(self.A) + 1 < len(self.B):
            ele = heapq.heappop(self.B)
            heapq.heappush(self.A, -ele)       # flip sign for max heap

    def findMedian(self) -> float:
        if len(self.A) == len(self.B):
            return (-self.A[0] + self.B[0]) / 2
        elif len(self.A) > len(self.B):
            return float(-self.A[0])
        else:
            return float(self.B[0])


# ============================================================
# 4. TWO HEAPS v2 — Push-Then-Fix  ★ BEST
# ============================================================
# Time:  addNum → O(log n)  |  findMedian → O(1)
# Space: O(n)
#
# How it works:
#   - A = max heap (lower half, stored as negatives)
#   - B = min heap (upper half)
#   - Three clear, ordered steps on every addNum:
#       Step 1 — Always push to A first (no routing logic).
#       Step 2 — Fix ordering: if max(A) > min(B), swap tops.
#       Step 3 — Fix sizes: A can have at most 1 extra element.
#
# Invariants maintained after every addNum:
#   1. max(A) <= min(B)         → all of A <= all of B
#   2. len(A) == len(B)
#      OR len(A) == len(B) + 1  → A holds the extra on odd count
#
# Why this is better than v1:
#   - Unconditional first push eliminates the "empty heap"
#     edge case entirely.
#   - Ordering and size balancing are separate sequential
#     steps — easy to reason about and debug.
#   - The invariant max(A) <= min(B) is explicitly enforced
#     in step 2, not just hoped for by routing.
#   - findMedian simplifies to a single branch because A is
#     always >= B in size.
# ============================================================
class TwoHeapMedianFinderV2:
    def __init__(self):
        self.A = []  # max heap (store negatives)
        self.B = []  # min heap

    def addNum(self, num: int) -> None:
        # Step 1: Always push to max heap first — no routing needed
        heapq.heappush(self.A, -num)

        # Step 2: Fix ordering — ensure max(A) <= min(B)
        #         If the new element broke that, swap the two tops.
        if self.B and -self.A[0] > self.B[0]:
            heapq.heappush(self.B, -heapq.heappop(self.A))

        # Step 3: Fix sizes — A can have at most 1 extra element
        if len(self.A) > len(self.B) + 1:
            heapq.heappush(self.B, -heapq.heappop(self.A))
        elif len(self.B) > len(self.A):
            heapq.heappush(self.A, -heapq.heappop(self.B))

    def findMedian(self) -> float:
        # A is always >= B in size, so only two cases exist
        if len(self.A) == len(self.B):
            return (-self.A[0] + self.B[0]) / 2
        return float(-self.A[0])  # A holds the extra element