from typing import List
import math

# ============================================================
# PROBLEM: Jump Game II (LeetCode 45)
# Start at index 0. nums[i] = max jump length from index i.
# Return the MINIMUM number of jumps to reach the last index.
# (Guaranteed you can always reach the last index)
# ============================================================


# ============================================================
# APPROACH 1: BRUTE FORCE (Recursion)
# Time: O(2^n)  |  Space: O(n) call stack
#
# From each index, try every possible jump.
# Return the minimum jumps across all paths.
# Explodes exponentially — massive recomputation.
# ============================================================
class SolutionBruteForce:
    def jump(self, nums: List[int]) -> int:
        def dfs(i):
            if i >= len(nums) - 1:
                return 0                         # already at/past end

            min_jumps = math.inf
            for jump in range(1, nums[i] + 1):  # try every jump length
                result = dfs(i + jump)
                min_jumps = min(min_jumps, 1 + result)

            return min_jumps

        return dfs(0)


# ============================================================
# APPROACH 2: MEMOIZATION (Top-Down DP)
# Time: O(n^2)  |  Space: O(n)
#
# Cache dfs(i) so each index is computed only once.
# Still explores all jumps from i, but no repeated work.
# ============================================================
class SolutionMemo:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        memo = {}

        def dfs(i):
            if i >= n - 1:
                return 0
            if i in memo:
                return memo[i]

            min_jumps = math.inf
            for jump in range(1, nums[i] + 1):
                result = dfs(i + jump)
                min_jumps = min(min_jumps, 1 + result)

            memo[i] = min_jumps
            return min_jumps

        return dfs(0)


# ============================================================
# APPROACH 3: BOTTOM-UP DP  ← your original solution
# Time: O(n^2)  |  Space: O(n)
#
# dp[i] = min jumps needed from index i to reach last index.
# Base case: dp[n-1] = 0 (already at end, 0 jumps needed).
# For each i (right to left):
#   Look at all reachable j in [i+1 .. i+nums[i]]
#   dp[i] = 1 + min(dp[j]) over all such j
#
# Example: nums = [2, 3, 1, 1, 4]
#   i=4: dp = [0, 0, 0, 0, 0]   base case
#   i=3: can reach j=4 → dp[3] = 1+dp[4] = 1
#   i=2: can reach j=3 → dp[2] = 1+dp[3] = 2
#   i=1: can reach j=2,3,4 → min(2,1,0) → dp[1] = 1+0 = 1
#   i=0: can reach j=1,2   → min(1,2)   → dp[0] = 1+1 = 2
#   Answer: 2  ✓
# ============================================================
class SolutionDP:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [0] * n                             # dp[n-1]=0 by default

        for i in range(n - 2, -1, -1):           # right → left
            farthest = min(n - 1, i + nums[i])
            min_required = math.inf
            for j in range(i + 1, farthest + 1):
                min_required = min(min_required, dp[j])
            dp[i] = 1 + min_required

        return dp[0]


# ============================================================
# APPROACH 4: BFS (Level-by-Level)
# Time: O(n)  |  Space: O(1)
#
# Think of jumps as BFS levels.
# Each "level" = all indices reachable in k jumps.
# Expand the frontier one level at a time.
#
# jumps=0  → indices reachable: [0]
# jumps=1  → indices reachable: [1..nums[0]]
# jumps=2  → indices reachable: [beyond prev frontier]
# ...stop when frontier covers last index.
#
# Track: current level's right boundary (cur_end)
#        farthest any node in this level can reach (farthest)
#
# Example: nums = [2, 3, 1, 1, 4]
#   jumps=0: cur_end=0
#   i=0: farthest=2, i==cur_end → jumps=1, cur_end=2
#   i=1: farthest=4
#   i=2: farthest=3, i==cur_end → jumps=2, cur_end=4 ≥ n-1 → stop
#   Answer: 2 ✓
# ============================================================
class SolutionBFS:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0

        jumps = 0
        cur_end = 0      # rightmost index of current BFS level
        farthest = 0     # farthest index reachable from current level

        for i in range(n - 1):          # don't need to jump FROM last index
            farthest = max(farthest, i + nums[i])

            if i == cur_end:            # exhausted current level → must jump
                jumps += 1
                cur_end = farthest
                if cur_end >= n - 1:    # already covers the end
                    break

        return jumps


# ============================================================
# APPROACH 5: GREEDY
# Time: O(n)  |  Space: O(1)
#
# At every position, greedily jump to whichever index
# allows you to reach the farthest next position.
#
# This is actually identical to BFS above in implementation
# but framed differently:
#   - within current jump window, track max reach
#   - when window expires, commit to next jump
# (BFS and Greedy converge to the same O(n) solution here)
# ============================================================


# ============================================================
# COMPLEXITY SUMMARY
# ─────────────────────────────────────────────────────────
#  Approach            Time        Space   Notes
# ─────────────────────────────────────────────────────────
#  Brute Force         O(2^n)      O(n)    TLE, massive overlap
#  Memoization         O(n^2)      O(n)    caches subproblems
#  Bottom-Up DP        O(n^2)      O(n)    iterative, your solution
#  BFS / Greedy        O(n)        O(1)    ← optimal
# ─────────────────────────────────────────────────────────
# ============================================================