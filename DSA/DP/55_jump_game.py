from typing import List

# ============================================================
# PROBLEM: Jump Game (LeetCode 55)
# Given array nums, start at index 0.
# nums[i] = max jump length from index i.
# Return True if you can reach the last index.
# ============================================================


# ============================================================
# APPROACH 1: BRUTE FORCE (Recursion)
# Time: O(2^n)  |  Space: O(n) call stack
#
# Try every possible jump from every index recursively.
# At each index, try all jump lengths from 1..nums[i].
# If any path reaches the last index → True.
# ============================================================
class SolutionBruteForce:
    def canJump(self, nums: List[int]) -> bool:
        def dfs(i):
            if i == len(nums) - 1:      # reached end
                return True
            if i >= len(nums) or nums[i] == 0:
                return False

            # try every jump length from current index
            for jump in range(1, nums[i] + 1):
                if dfs(i + jump):
                    return True
            return False

        return dfs(0)


# ============================================================
# APPROACH 2: MEMOIZATION (Top-Down DP)
# Time: O(n^2)  |  Space: O(n)
#
# Same as brute force but cache results per index.
# Each index is computed once → eliminates recomputation.
# ============================================================
class SolutionMemo:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        memo = {}

        def dfs(i):
            if i in memo:
                return memo[i]
            if i >= n - 1:
                return True
            if nums[i] == 0:
                return False

            for jump in range(1, nums[i] + 1):
                if dfs(i + jump):
                    memo[i] = True
                    return True

            memo[i] = False
            return False

        return dfs(0)


# ============================================================
# APPROACH 3: BOTTOM-UP DP  ← your original solution
# Time: O(n^2)  |  Space: O(n)
#
# dp[i] = True if index i can reach the last index.
# Base case: dp[n-1] = True (already at end).
# For each index i (right to left):
#   Look at all reachable indices j from i.
#   If any dp[j] is True → dp[i] = True.
# Answer is dp[0].
#
#   i=0   i=1   i=2   i=3   i=4
# [ 2,    3,    1,    1,    0  ]
#   dp: [T,    T,    T,    F,    T]
#       ↑ answer                ↑ base
# ============================================================
class SolutionDP:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        dp = [False] * n
        dp[n - 1] = True                        # base case

        for i in range(n - 2, -1, -1):          # right → left
            farthest = min(n - 1, i + nums[i])  # don't go out of bounds
            for j in range(i + 1, farthest + 1):
                if dp[j]:                        # found a reachable winning index
                    dp[i] = True
                    break                        # no need to check further

        return dp[0]


# ============================================================
# APPROACH 4: GREEDY (Optimal)
# Time: O(n)  |  Space: O(1)
#
# Key insight: track the farthest index reachable so far.
# Scan left to right. At each index i:
#   - If i > max_reach → we're stranded, return False.
#   - Otherwise update max_reach = max(max_reach, i + nums[i])
# If we finish the loop → True.
#
# Example: [2, 3, 1, 1, 0]
#   i=0: max_reach = max(0, 0+2) = 2
#   i=1: max_reach = max(2, 1+3) = 4  ✓ (covers last index)
#   i=2: max_reach = max(4, 2+1) = 4
#   → return True
#
# Example: [3, 2, 1, 0, 4]
#   i=0: max_reach = 3
#   i=1: max_reach = 3
#   i=2: max_reach = 3
#   i=3: max_reach = 3
#   i=4: 4 > 3 → return False ✗
# ============================================================
class SolutionGreedy:
    def canJump(self, nums: List[int]) -> bool:
        max_reach = 0

        for i in range(len(nums)):
            if i > max_reach:       # can't reach index i
                return False
            max_reach = max(max_reach, i + nums[i])

        return True


# ============================================================
# COMPLEXITY SUMMARY
# ─────────────────────────────────────────────────────────
#  Approach            Time        Space   Notes
# ─────────────────────────────────────────────────────────
#  Brute Force         O(2^n)      O(n)    TLE on large input
#  Memoization         O(n^2)      O(n)    caches subproblems
#  Bottom-Up DP        O(n^2)      O(n)    iterative, no stack
#  Greedy              O(n)        O(1)    ← optimal
# ─────────────────────────────────────────────────────────
# ============================================================