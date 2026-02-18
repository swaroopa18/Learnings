# https://leetcode.com/problems/min-cost-climbing-stairs/description/
from typing import List


# ============================================================================
# APPROACH 1: NAIVE RECURSION (Brute Force)
# ============================================================================
# At each step i, we pay cost[i] and then choose to jump 1 or 2 steps.
# We want the minimum total cost to reach "beyond" the last step.
# Start from either step 0 or step 1 (we can begin at either).
#
# Time Complexity:  O(2^n) - each call branches into 2 recursive calls
# Space Complexity: O(n)   - recursion call stack depth
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        def dfs(i):
            if i >= len(cost):
                return 0
            return cost[i] + min(dfs(i + 1), dfs(i + 2))

        return min(dfs(0), dfs(1))


# ============================================================================
# APPROACH 2: TOP-DOWN DP (Memoized Recursion)
# ============================================================================
# Same recursion as above, but we cache results in a memo dict to avoid
# recomputing overlapping subproblems.
#
# Time Complexity:  O(n) - each index computed once
# Space Complexity: O(n) - memo dict + recursion call stack
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        memo = {}

        def dfs(i):
            if i >= len(cost):
                return 0
            if i in memo:
                return memo[i]
            memo[i] = cost[i] + min(dfs(i + 1), dfs(i + 2))
            return memo[i]

        return min(dfs(0), dfs(1))


# ============================================================================
# APPROACH 3: BOTTOM-UP DP (Tabulation)
# ============================================================================
# Build the solution iteratively from the base cases upward.
# dp[i] = minimum cost to reach step i.
#
# Recurrence:
#   dp[i] = cost[i] + min(dp[i-1], dp[i-2])
#
# Answer: min(dp[n-1], dp[n-2])
#   → because we can reach the top from either of the last two steps.
#
# Time Complexity:  O(n) - single pass through array
# Space Complexity: O(n) - DP array of size n
class Solution1:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)

        if n <= 2:
            return min(cost)

        dp = [0] * n
        dp[0] = cost[0]
        dp[1] = cost[1]

        for i in range(2, n):
            dp[i] = cost[i] + min(dp[i - 1], dp[i - 2])

        return min(dp[n - 1], dp[n - 2])


# ============================================================================
# APPROACH 4: SPACE-OPTIMIZED BOTTOM-UP DP ✓ BEST
# ============================================================================
# Since dp[i] only depends on the previous two values, we don't need the
# full array — just two rolling variables.
#
# two_steps_back = dp[i-2]
# one_step_back  = dp[i-1]
#
# Time Complexity:  O(n) - single pass
# Space Complexity: O(1) - only two variables
class Solution2Improved:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)

        if n <= 2:
            return min(cost)

        two_steps_back = cost[0]
        one_step_back = cost[1]

        for i in range(2, n):
            current = cost[i] + min(one_step_back, two_steps_back)
            two_steps_back = one_step_back
            one_step_back = current

        # Final answer: cheapest of reaching the top from the last two steps
        return min(one_step_back, two_steps_back)