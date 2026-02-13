import math
from typing import List
from bisect import bisect_left

# ============================================================
# APPROACH 1: Brute Force Recursion
# Time: O(2^n) | Space: O(n) — recursion stack
# Explores every subset by choosing to take or skip each element
# ============================================================
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        def backtrack(index, prev, length):
            # Base case: reached end of array
            if index == len(nums):
                return length

            # Option 1: Skip current element
            skip = backtrack(index + 1, prev, length)

            # Option 2: Take current element only if it extends the sequence
            take = 0
            if nums[index] > prev:
                take = backtrack(index + 1, nums[index], length + 1)

            return max(take, skip)

        return backtrack(0, -math.inf, 0)

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        maxLength = 0
        n = len(nums)

        def helper(idx, prev, length):
            nonlocal maxLength
            if idx == n:
                maxLength = max(maxLength, length)
                return
            if nums[idx] > prev:
                helper(idx + 1, nums[idx], length + 1)
            helper(idx + 1, prev, length)

        helper(0, -math.inf, 0)
        return maxLength

# ============================================================
# APPROACH 2: Top-Down DP (Memoization)
# Time: O(n^2) | Space: O(n^2) — memo table
# Key insight: track index of previous element instead of its
# value — this gives us a hashable, bounded memo key
# ============================================================
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        memo = {}

        def dfs(i, prev_idx):
            if i == len(nums):
                return 0
            if (i, prev_idx) in memo:
                return memo[(i, prev_idx)]

            # Always allowed to skip
            not_take = dfs(i + 1, prev_idx)

            # Take only if current element is greater than previous
            take = 0
            if prev_idx == -1 or nums[i] > nums[prev_idx]:
                take = 1 + dfs(i + 1, i)

            memo[(i, prev_idx)] = max(take, not_take)
            return memo[(i, prev_idx)]

        return dfs(0, -1)  # -1 sentinel = no previous element chosen


# ============================================================
# APPROACH 3: Bottom-Up DP (Tabulation)
# Time: O(n^2) | Space: O(n)
# dp[i] = length of LIS ending at index i
# Every element starts as a sequence of length 1 (itself)
# For each i, look back at all j < i to find valid extensions
# ============================================================
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [1] * n  # Every element is an LIS of length 1 on its own

        for i in range(n):
            for j in range(i):           # Check all previous elements
                if nums[i] > nums[j]:    # Can extend the subsequence at j
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)


# ============================================================
# APPROACH 4: Binary Search (Patience Sort / Greedy)
# Time: O(n log n) | Space: O(n)
# OPTIMAL SOLUTION
#
# Maintain a `tails` array where tails[i] is the SMALLEST
# possible tail element of all increasing subsequences of length i+1.
#
# For each number:
#   - If it's larger than all tails → extend LIS by 1
#   - Otherwise → binary search for the leftmost tail >= num
#     and replace it with num (greedy: smaller tail = more room to grow)
#
# Note: tails is always sorted, but does NOT represent the actual LIS.
# Its LENGTH equals the LIS length.
# ============================================================
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []  # tails[i] = smallest tail for IS of length i+1

        for num in nums:
            pos = bisect_left(tails, num)   # Find leftmost position where tails[pos] >= num

            if pos == len(tails):
                tails.append(num)           # num extends the longest sequence found so far
            else:
                tails[pos] = num            # Replace to keep tails as small as possible

        return len(tails)


# ============================================================
# APPROACH 5: Bottom-Up DP with actual LIS reconstruction
# Time: O(n^2) | Space: O(n)
# Same DP as Approach 3, but also tracks the previous index
# so we can reconstruct the actual subsequence
# ============================================================
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [1] * n
        parent = [-1] * n   # parent[i] = index of previous element in LIS ending at i

        for i in range(n):
            for j in range(i):
                if nums[i] > nums[j] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j

        # Reconstruct the LIS
        max_len = max(dp)
        idx = dp.index(max_len)
        lis = []
        while idx != -1:
            lis.append(nums[idx])
            idx = parent[idx]

        lis.reverse()
        print("Actual LIS:", lis)  # e.g. [2, 3, 7, 101]
        return max_len


# ============================================================
# COMPLEXITY SUMMARY
# ============================================================
# Approach                  Time        Space   Notes
# --------------------------------------------------------
# 1. Brute Force Recursion  O(2^n)      O(n)    TLE on large inputs
# 2. Top-Down DP (Memo)     O(n^2)      O(n^2)  Clean recursive structure
# 3. Bottom-Up DP           O(n^2)      O(n)    Iterative, cache-friendly
# 4. Binary Search (Greedy) O(n log n)  O(n)    OPTIMAL — use in interviews
# 5. DP + Reconstruction    O(n^2)      O(n)    Use when actual LIS is needed