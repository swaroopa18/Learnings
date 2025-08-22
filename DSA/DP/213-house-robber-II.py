from typing import List

# APPROACH 1: Space-Optimized Dynamic Programming (BEST APPROACH)

class Solution:
    """
    House Robber II - LeetCode Problem
    
    Problem: Houses are arranged in a circle. You cannot rob two adjacent houses.
    Find the maximum amount you can rob without alerting police.
    
    Time Complexity: O(n) - Single pass through the array twice
    Space Complexity: O(1) - Only using constant extra space
    
    Approach: Since houses form a circle, we have two scenarios:
    1. Rob houses 0 to n-2 (exclude last house)
    2. Rob houses 1 to n-1 (exclude first house)
    Take maximum of both scenarios.
    """
    
    def rob_linear(self, houses):
        """
        Helper function to solve linear house robber problem.
        
        Time: O(n), Space: O(1)
        """
        if not houses:
            return 0
        if len(houses) == 1:
            return houses[0]
            
        prev1, prev2 = houses[0], 0
        
        for i in range(1, len(houses)):
            current = max(prev2 + houses[i], prev1)
            prev2 = prev1
            prev1 = current
            
        return prev1

    def rob(self, nums: List[int]) -> int:
        """
        Time Complexity: O(n) - Two linear passes
        Space Complexity: O(1) - Constant extra space
        """
        n = len(nums)
        
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[0], nums[1])
        
        # Scenario 1: Rob houses 0 to n-2 (can't rob last house if rob first)
        # Scenario 2: Rob houses 1 to n-1 (can't rob first house if rob last)
        scenario1 = self.rob_linear(nums[:-1])  # Exclude last house
        scenario2 = self.rob_linear(nums[1:])   # Exclude first house
        
        return max(scenario1, scenario2)

# APPROACH 2: Dynamic Programming with Arrays (Less Space Efficient)

class SolutionDP:
    """
    Time: O(n), Space: O(n) - uses additional arrays
    """
    
    def rob_linear_dp(self, houses):
        if not houses:
            return 0
        if len(houses) == 1:
            return houses[0]
            
        n = len(houses)
        dp = [0] * n
        dp[0] = houses[0]
        dp[1] = max(houses[0], houses[1])
        
        for i in range(2, n):
            dp[i] = max(dp[i-1], dp[i-2] + houses[i])
            
        return dp[n-1]
    
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[0], nums[1])
            
        return max(self.rob_linear_dp(nums[:-1]), 
                  self.rob_linear_dp(nums[1:]))

# APPROACH 3: Recursive with Memoization

class SolutionRecursiveMemo:
    """
    Recursive approach with memoization
    
    Time: O(n), Space: O(n) - recursion stack + memoization
    Good for understanding the problem structure
    """
    
    def rob_helper(self, houses, i, memo):
        if i >= len(houses):
            return 0
        if i in memo:
            return memo[i]
            
        # Either rob current house or skip it
        rob_current = houses[i] + self.rob_helper(houses, i + 2, memo)
        skip_current = self.rob_helper(houses, i + 1, memo)
        
        memo[i] = max(rob_current, skip_current)
        return memo[i]
    
    def rob_linear_memo(self, houses):
        return self.rob_helper(houses, 0, {})
    
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[0], nums[1])
            
        return max(self.rob_linear_memo(nums[:-1]), 
                  self.rob_linear_memo(nums[1:]))
# Key Insights:
# 1. Circular constraint creates two mutually exclusive scenarios
# 2. Each scenario reduces to linear house robber problem
# 3. Space optimization: only need last two DP values, not entire array
# 4. This problem demonstrates how constraints can be handled by case analysis