from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        # Time Complexity: O(n) - single pass through the array
        # Space Complexity: O(n) - using dp array of size n+1
        
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]

        # dp[i] represents max money that can be robbed from houses 0 to i-1
        dp = [0] * (n + 1)
        dp[1] = nums[0]  # base case: only first house

        for i in range(2, n + 1):
            # Either rob current house + best from i-2, or skip current house
            dp[i] = max(dp[i - 2] + nums[i - 1], dp[i - 1])

        return dp[n]
    
    class Solution:
        def rob(self, nums: List[int]) -> int:
            n = len(nums)
            dp = [0] * (n + 1)
            dp[1] = nums[0]
            for i in range(1, n):
                dp[i + 1] = max(dp[i - 1] + nums[i], dp[i])
            return dp[-1]

    # IMPROVED VERSION - Space Optimized
    def rob_optimized(self, nums: List[int]) -> int:
        # Time Complexity: O(n) - single pass through the array
        # Space Complexity: O(1) - only using two variables instead of array
        
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
        
        prev2 = 0        # dp[i-2]
        prev1 = nums[0]  # dp[i-1]
        
        for i in range(1, n):
            current = max(prev2 + nums[i], prev1)
            prev2 = prev1
            prev1 = current
            
        return prev1
    
class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        before_prev, prev = 0, 0
        for num in nums:
            curr = max(before_prev + num, prev)
            before_prev = prev
            prev = curr
        return prev

    # ALTERNATIVE IMPROVED VERSION - Even cleaner
    def rob_cleanest(self, nums: List[int]) -> int:
        # Time Complexity: O(n)
        # Space Complexity: O(1)
        
        # rob = max money including current house
        # not_rob = max money excluding current house
        rob = not_rob = 0
        
        for money in nums:
            # If we rob current house, add to previous not_rob
            # If we don't rob, take max of previous rob/not_rob
            rob, not_rob = not_rob + money, max(rob, not_rob)
            
        return max(rob, not_rob)