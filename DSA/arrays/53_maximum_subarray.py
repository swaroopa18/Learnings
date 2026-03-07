"""
============================================================
MAXIMUM SUBARRAY — LeetCode #53
============================================================
Problem:
    Given an integer array `nums`, find the subarray with
    the largest sum and return that sum.

Example:
    Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    Output: 6
    Reason: Subarray [4, -1, 2, 1] has the largest sum = 6

Constraints:
    - 1 <= nums.length <= 100,000
    - -10,000 <= nums[i] <= 10,000
============================================================
"""

import math
from typing import List


# ============================================================
# APPROACH 1 — Brute Force  (Original Solution)
# ============================================================
# Idea:
#   Try every possible subarray by using two nested loops.
#   The outer loop picks the start index i, and the inner
#   loop expands the window to the right (index j), keeping
#   a running sum and updating the global max.
#
# Why it works:
#   Exhaustively checks ALL subarrays, so the answer is
#   guaranteed to be found.
#
# Drawback:
#   For every new start i, we recompute sums from scratch,
#   resulting in a lot of repeated work.
#
# Time Complexity  : O(n²) — two nested loops over n elements
# Space Complexity : O(1)  — only two extra variables used
# ============================================================

class SolutionBruteForce:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = -math.inf

        for i in range(len(nums)):          # pick start index
            curr_sum = 0
            for j in range(i, len(nums)):   # expand window to the right
                curr_sum += nums[j]
                max_sum = max(max_sum, curr_sum)

        return max_sum


# ============================================================
# APPROACH 2 — Kadane's Algorithm  (Original Optimised Solution)
# ============================================================
# Idea:
#   Scan the array once. At each element, we decide:
#     • Extend the existing subarray  → curr_sum += nums[i]
#     • OR start fresh from here      → reset curr_sum = 0
#
#   The reset happens when curr_sum drops to 0 or below,
#   because a negative-or-zero prefix can only hurt any
#   future subarray sum — it's better to start fresh.
#
# Why it works:
#   At every index i, curr_sum represents the best subarray
#   sum ending at i. Taking the running max of those values
#   gives the global best.
#
# Key insight:
#   We never need to look back. If the running sum becomes
#   non-positive, we simply discard everything seen so far
#   and treat the next element as a new starting point.
#
#  If the running sum becomes negative or zero,
#  it will only reduce future sums, so we reset it.
#
# Time Complexity  : O(n) — single pass through the array
# Space Complexity : O(1) — only two variables used
# ============================================================

class SolutionKadane:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = -math.inf
        curr_sum = 0

        for i in range(len(nums)):
            curr_sum += nums[i]
            max_sum = max(max_sum, curr_sum)  # update global best

            if curr_sum <= 0:
                curr_sum = 0    # negative prefix is useless — reset

        return max_sum


# ============================================================
# APPROACH 3 — Kadane's (Cleaner pythonic variant)
# ============================================================
# Same algorithm as Approach 2, written more concisely.
# Also tracks the actual subarray indices so you can
# recover WHICH subarray produced the max sum.
#
# Time Complexity  : O(n)
# Space Complexity : O(1)
# ============================================================

class SolutionKadaneClean:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum  = nums[0]   # handles all-negative arrays safely
        curr_sum = nums[0]

        for num in nums[1:]:
            # Either extend the current subarray or start fresh at `num`
            curr_sum = max(num, curr_sum + num)
            max_sum  = max(max_sum, curr_sum)

        return max_sum

    def maxSubArrayWithIndices(self, nums: List[int]) -> tuple:
        """Returns (max_sum, start_index, end_index) of the best subarray."""
        max_sum  = nums[0]
        curr_sum = nums[0]
        start = end = 0
        temp_start = 0          # candidate start for the current window

        for i in range(1, len(nums)):
            if curr_sum + nums[i] < nums[i]:
                curr_sum   = nums[i]
                temp_start = i  # starting a fresh window here
            else:
                curr_sum += nums[i]

            if curr_sum > max_sum:
                max_sum = curr_sum
                start   = temp_start
                end     = i

        return max_sum, start, end


# ============================================================
# APPROACH 4 — Divide & Conquer
# ============================================================
# Idea:
#   Split the array in half recursively. The max subarray
#   must lie entirely in:
#     (a) the LEFT  half, OR
#     (b) the RIGHT half, OR
#     (c) CROSSING the midpoint (touches both halves)
#
#   Cases (a) and (b) are solved recursively.
#   Case  (c) is solved in O(n) by expanding outward from
#   the midpoint in both directions and summing.
#
# Why it works:
#   Every possible subarray falls into exactly one of the
#   three cases above, so the correct answer is always found.
#
# When to use:
#   Useful when you need to practise D&C thinking, or in
#   parallel / distributed settings where each half can be
#   processed independently.
#
# Time Complexity  : O(n log n) — log n levels, O(n) per level
# Space Complexity : O(log n)   — recursion call stack depth
# ============================================================

class SolutionDivideAndConquer:
    def maxSubArray(self, nums: List[int]) -> int:
        return self._helper(nums, 0, len(nums) - 1)

    def _helper(self, nums: List[int], left: int, right: int) -> int:
        if left == right:
            return nums[left]   # base case: single element

        mid = (left + right) // 2

        left_max  = self._helper(nums, left, mid)       # best in left half
        right_max = self._helper(nums, mid + 1, right)  # best in right half
        cross_max = self._crossSum(nums, left, right, mid)  # best crossing mid

        return max(left_max, right_max, cross_max)

    def _crossSum(self, nums: List[int], left: int, right: int, mid: int) -> int:
        # Expand LEFT from mid
        left_sum = best_left = -math.inf
        for i in range(mid, left - 1, -1):
            left_sum += nums[i]
            best_left = max(best_left, left_sum)

        # Expand RIGHT from mid+1
        right_sum = best_right = -math.inf
        for i in range(mid + 1, right + 1):
            right_sum += nums[i]
            best_right = max(best_right, right_sum)

        return best_left + best_right   # cross subarray sum


# ============================================================
# APPROACH 5 — Dynamic Programming (Explicit DP Table)
# ============================================================
# Idea:
#   Define dp[i] = maximum subarray sum ENDING at index i.
#
#   Recurrence:
#     dp[i] = max(nums[i], dp[i-1] + nums[i])
#
#   Translation:
#     Either start a brand-new subarray at i  → nums[i]
#     Or extend the best subarray ending at i-1 → dp[i-1] + nums[i]
#
#   Answer = max(dp)
#
# Note:
#   This is mathematically identical to Kadane's Algorithm.
#   Kadane's is simply the space-optimised version of this DP,
#   where we discard the table and keep only the last value.
#
# Time Complexity  : O(n)
# Space Complexity : O(n) — stores the full dp table
#                   (reducible to O(1) by keeping only dp[i-1])
# ============================================================

class SolutionDP:
    def maxSubArray(self, nums: List[int]) -> int:
        dp = [0] * len(nums)
        dp[0] = nums[0]

        for i in range(1, len(nums)):
            dp[i] = max(nums[i], dp[i - 1] + nums[i])

        return max(dp)


# ============================================================
# COMPLEXITY COMPARISON SUMMARY
# ============================================================
#
#  Approach               | Time     | Space  | Notes
#  -----------------------+----------+--------+-------------------
#  Brute Force            | O(n²)    | O(1)   | Too slow for n>10k
#  Kadane's Algorithm     | O(n)     | O(1)   | ✅ Optimal — use this
#  Kadane's (clean)       | O(n)     | O(1)   | ✅ Pythonic + indices
#  Divide & Conquer       | O(n logn)| O(logn)| Good for D&C practice
#  Dynamic Programming    | O(n)     | O(n)   | Explicit DP formulation
#
# ✅ Recommended: Approach 3 (Kadane's Clean) for interviews.
#    It's O(n) time, O(1) space, and can also return indices.
# ============================================================