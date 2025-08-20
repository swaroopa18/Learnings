# https://leetcode.com/problems/min-cost-climbing-stairs/description/
from typing import List

# ============================================================================
# SOLUTION 1: BOTTOM-UP DP WITH ARRAY
# ============================================================================
class Solution1:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        Time Complexity: O(n) - single pass through array
        Space Complexity: O(n) - DP array of size n        
        """
        n = len(cost)
        
        # Handle edge cases
        if n <= 2:
            return min(cost)
        
        dp = [0] * n
        dp[0] = cost[0]  # Cost to reach step 0
        dp[1] = cost[1]  # Cost to reach step 1
        
        for i in range(2, n):
            dp[i] = cost[i] + min(dp[i - 1], dp[i - 2])
        
        return min(dp[n - 1], dp[n - 2])

# ============================================================================
# SOLUTION 2: SPACE-OPTIMIZED DP (BEST)
# ============================================================================
class Solution2Improved:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        n = len(cost)
        
        if n <= 2:
            return min(cost)
        
        two_steps_back = cost[0]
        one_step_back = cost[1]
        
        for i in range(2, n):
            current = cost[i] + min(one_step_back, two_steps_back)
            two_steps_back = one_step_back
            one_step_back = current
        
        return min(one_step_back, two_steps_back)