"""
============================================================
MAJORITY ELEMENT - LeetCode #169
============================================================
Problem: Given an array nums of size n, return the majority
element (appears more than n // 2 times). Guaranteed to exist.
============================================================
"""

from typing import List
from collections import Counter


# ─────────────────────────────────────────────
# Solution 1: HashMap / Frequency Count
# Time: O(n) | Space: O(n)
# ─────────────────────────────────────────────
# Counts frequencies in a dict, returns early
# once an element crosses the majority threshold.
# Early exit is a nice optimization but space
# grows with the number of unique elements.
# ─────────────────────────────────────────────
class Solution1:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        hmap = {}
        for num in nums:
            hmap[num] = hmap.get(num, 0) + 1
            if hmap[num] > n // 2:   # simplified from >= (n//2)+1
                return num


# ─────────────────────────────────────────────
# Solution 2: Boyer-Moore Voting ✅ OPTIMAL
# Time: O(n) | Space: O(1)
# ─────────────────────────────────────────────
# Core insight: cancel every majority element
# with a non-majority element — the majority
# element still survives because it appears
# more than n//2 times and can never be
# fully cancelled out.
#
# Think of it as a battle:
#   - Same as candidate  → count +1 (ally)
#   - Different          → count -1 (enemy cancels)
#   - count hits 0       → pick a new candidate
#
# Trace on [2, 2, 1, 1, 2]:
#   num=2 → candidate=2, count=1
#   num=2 → candidate=2, count=2
#   num=1 → candidate=2, count=1
#   num=1 → candidate=2, count=0
#   num=2 → candidate=2, count=1  ✅
# ─────────────────────────────────────────────
class Solution2:
    def majorityElement(self, nums: List[int]) -> int:
        count = 0
        candidate = None
        for num in nums:
            if count == 0:
                candidate = num
                count += 1
            elif num == candidate:
                count += 1
            else:
                count -= 1
        return candidate


# ─────────────────────────────────────────────
# Solution 3: collections.Counter (Pythonic)
# Time: O(n) | Space: O(n)
# ─────────────────────────────────────────────
# Clean and readable. most_common(1) returns
# the single most frequent element as a list
# of (element, count) tuples.
# Great for a quick first pass in interviews.
# ─────────────────────────────────────────────
class Solution3:
    def majorityElement(self, nums: List[int]) -> int:
        return Counter(nums).most_common(1)[0][0]


# ─────────────────────────────────────────────
# Solution 4: Sort + Middle Index
# Time: O(n log n) | Space: O(1)
# ─────────────────────────────────────────────
# Since majority element appears > n//2 times,
# after sorting it is guaranteed to sit at
# index n//2. Clever but slower than O(n).
# ─────────────────────────────────────────────
class Solution4:
    def majorityElement(self, nums: List[int]) -> int:
        nums.sort()
        return nums[len(nums) // 2]


# ─────────────────────────────────────────────
# COMPARISON SUMMARY
# ─────────────────────────────────────────────
# | Solution        | Time      | Space | Notes               |
# |-----------------|-----------|-------|---------------------|
# | HashMap         | O(n)      | O(n)  | Early exit bonus    |
# | Boyer-Moore     | O(n)      | O(1)  | ✅ Optimal          |
# | Counter         | O(n)      | O(n)  | Most readable       |
# | Sort + mid      | O(n logn) | O(1)  | Clever but slower   |
#
# KEY TAKEAWAY:
# Boyer-Moore is the gold standard answer for interviews.
# HashMap is the natural first instinct and perfectly valid.
# Note: Boyer-Moore only works if a majority element is
# GUARANTEED to exist. If not, add a verification pass.
# ─────────────────────────────────────────────
