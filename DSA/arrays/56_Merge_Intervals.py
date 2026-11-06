"""
LeetCode 56 - Merge Intervals
------------------------------
Given an array of `intervals` where intervals[i] = [start_i, end_i], merge
all overlapping intervals and return an array of the non-overlapping
intervals that cover all the intervals in the input.

Nine approaches are given below.

Summary
-------
 #  Approach                       Time          Space     Notes
 1  Brute force (repeat merging)   O(n^3)        O(n)      Easiest to reason about, far too slow
 2  Graph + DFS                    O(n^2)        O(n^2)    Overlap = edge, answer = components
 3  Union-Find (DSU)               O(n^2 a(n))   O(n)      Same idea as 2, no explicit graph
 4  Sort + Sweep (your version)    O(n log n)    O(n)      Classic, optimal
 5  Sort + result[-1] (BEST)       O(n log n)    O(n)      Cleanest form of 4 (stack formulation)
 6  Sort starts/ends separately    O(n log n)    O(n)      Neat trick, no pair sorting
 7  Sweep line with events         O(n log n)    O(n)      Generalizes to "max overlap" problems
 8  Difference array (bucket)      O(n + R)      O(R)      R = coordinate range; great if R is small
 9  Divide and conquer             O(n log n)    O(n)      Merge-sort style

Overlap test used everywhere: two intervals a and b overlap (or touch) when
    a[0] <= b[1] and b[0] <= a[1]
Touching intervals such as [1, 4] and [4, 5] DO merge into [1, 5].
"""

from collections import defaultdict
from typing import List


class SolutionBruteForce:
    """
    Approach 1: Brute Force (repeat pairwise merging until stable)
    ----------------------------------------------------------------
    Idea:
      - Take each interval and absorb every other interval that overlaps
        it, growing the current interval as it absorbs.
      - A single pass is NOT enough: after interval i grows, an interval
        j < i that was skipped earlier may now overlap it. So repeat full
        passes until a pass performs no merges.

    Time Complexity:  O(n^3) -- each pass is O(n^2) and there can be up to
                                O(n) passes (e.g. a chain that collapses one
                                link per pass).
    Space Complexity: O(n)

    Good for building intuition. Too slow for n = 10^4.
    """

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        result = [list(i) for i in intervals]
        merged_any = True

        while merged_any:
            merged_any = False
            used = [False] * len(result)
            next_round = []

            for i in range(len(result)):
                if used[i]:
                    continue
                cur = result[i]
                for j in range(i + 1, len(result)):
                    if used[j]:
                        continue
                    if cur[0] <= result[j][1] and result[j][0] <= cur[1]:
                        cur = [min(cur[0], result[j][0]), max(cur[1], result[j][1])]
                        used[j] = True
                        merged_any = True
                next_round.append(cur)

            result = next_round

        return sorted(result)

class SolutionSortAndSweep:
    """
    Approach 4: Sort + Sweep (your version, annotated)
    ----------------------------------------------------
    Idea:
      - Sort intervals by start time. After sorting, any intervals that
        overlap must be next to each other, so one left-to-right pass is
        enough.
      - Keep a "current" interval (newInterval). For each next interval:
          * If it starts at or before the current one ends
            (interval[0] <= newInterval[1]), they overlap: extend the
            current interval's end to max(both ends). The max matters
            because the next interval can be fully contained, e.g.
            [1, 10] and [2, 3] -> the end must stay 10, not become 3.
          * Otherwise there is a gap: the current interval is final, so
            push it to the result and start a new current interval.
      - After the loop, the last "current" interval has not been pushed
        yet, so append it.

    Time Complexity:  O(n log n) -- dominated by the sort; the sweep is O(n).
    Space Complexity: O(n)       -- for the result list.

    Small things to be aware of:
      - `intervals.sort()` sorts the caller's list IN PLACE.
      - `newInterval = interval` aliases the input list. Safe here since it
        is only re-assigned, never mutated.
    """

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals) <= 1:
            return intervals

        result = []
        intervals.sort()

        newInterval = intervals[0]

        for interval in intervals[1:]:
            if interval[0] <= newInterval[1]:
                newInterval = [newInterval[0], max(interval[1], newInterval[1])]
            else:
                result.append(newInterval)
                newInterval = interval
        result.append(newInterval)
        return result


class Solution:
    """
    Approach 5 (RECOMMENDED): Sort + Sweep using result[-1] (stack form)
    ----------------------------------------------------------------------
    Idea:
      - Same algorithm as Approach 4, but always treat the LAST interval in
        `result` as the current one. `result` doubles as a stack.
      - For each interval in sorted order:
          * If result is empty or there's no overlap
            (start > result[-1][1]), push it.
          * Otherwise, merge by extending the end of result[-1] in place.

    Why it's cleaner:
      - No special case for 0/1 intervals (empty input returns []).
      - No leftover "append the last one after the loop" step.
      - No aliasing with input lists, and `sorted()` leaves the input alone.

    Time Complexity:  O(n log n) -- sorting dominates; the sweep is O(n).
    Space Complexity: O(n)       -- output plus the sorted copy.
    """

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        result: List[List[int]] = []

        for start, end in sorted(intervals):
            if not result or start > result[-1][1]:
                result.append([start, end])
            else:
                result[-1][1] = max(result[-1][1], end)

        return result


class SolutionDifferenceArray:
    """
    Approach 8: Difference Array (bucket / counting)
    --------------------------------------------------
    Idea:
      - If coordinates are small integers, skip sorting: mark coverage in a
        difference array, then take a running sum to see which points are
        covered.
      - Problem: with plain integer points, [1, 2] and [3, 4] would look
        adjacent and wrongly merge. Fix: DOUBLE every coordinate. Interval
        [s, e] covers positions 2s .. 2e (inclusive), so a real gap between
        2 and 3 leaves position 5 uncovered, while touching intervals
        ([1, 4], [4, 5]) share position 8 and stay connected.
      - diff[2s] += 1 and diff[2e + 1] -= 1. Scan the running sum:
        0 -> positive starts a block, positive -> 0 ends one.
      - Coordinates are shifted by the minimum start so negatives work.

    Time Complexity:  O(n + R) -- R = max end - min start (the range).
    Space Complexity: O(R)

    Beats sorting only when R is small relative to n log n. For huge or
    sparse ranges (e.g. up to 10^9), use a sort-based approach instead.
    """

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []

        low = min(i[0] for i in intervals)
        high = max(i[1] for i in intervals)
        size = 2 * (high - low) + 2
        diff = [0] * size

        for start, end in intervals:
            diff[2 * (start - low)] += 1
            diff[2 * (end - low) + 1] -= 1

        result = []
        cover = 0
        block_start = 0

        for pos in range(size):
            prev = cover
            cover += diff[pos]
            if prev == 0 and cover > 0:
                block_start = pos // 2 + low
            elif prev > 0 and cover == 0:
                result.append([block_start, (pos - 1) // 2 + low])

        return result


class SolutionDivideAndConquer:
    """
    Approach 9: Divide and Conquer (merge-sort style)
    ---------------------------------------------------
    Idea:
      - Split the list in half, recursively merge each half into a sorted
        list of disjoint intervals, then combine the two results.
      - Combining is like the merge step of merge sort: repeatedly take the
        interval with the smaller start from either list, and either append
        it or fold it into the last interval of the output.

    Time Complexity:  O(n log n) -- log n levels, O(n) combine per level.
    Space Complexity: O(n)       -- output lists, plus O(log n) recursion.

    No up-front global sort, and the combine step is handy when the two
    halves arrive already merged (e.g. distributed / streaming data).
    """

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals) <= 1:
            return [list(i) for i in intervals]

        mid = len(intervals) // 2
        left = self.merge(intervals[:mid])
        right = self.merge(intervals[mid:])
        return self._combine(left, right)

    @staticmethod
    def _combine(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
        i = j = 0
        out: List[List[int]] = []

        while i < len(a) or j < len(b):
            if j >= len(b) or (i < len(a) and a[i][0] <= b[j][0]):
                nxt = a[i]
                i += 1
            else:
                nxt = b[j]
                j += 1

            if out and nxt[0] <= out[-1][1]:
                out[-1][1] = max(out[-1][1], nxt[1])
            else:
                out.append([nxt[0], nxt[1]])

        return out