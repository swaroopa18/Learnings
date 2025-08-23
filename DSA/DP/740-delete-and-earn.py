# https://leetcode.com/problems/delete-and-earn/description/

from typing import List

# ============================================================================
# PROBLEM: Delete and Earn
# Pick any nums[i] and earn nums[i] points, but delete all instances of 
# nums[i] - 1 and nums[i] + 1. Find maximum points you can earn.
# ============================================================================

# ============================================================================
# SOLUTION 1: DP WITH ARRAY
# ============================================================================
class Solution1:
    def deleteAndEarn(self, nums: List[int]) -> int:
        """
        Time Complexity: O(n log n) - sorting dominates
        Space Complexity: O(n) - freq dict + unique_nums + dp array
        
        Logic:
        - If we take current number, we can't take previous consecutive number
        - If numbers are consecutive: dp[i] = max(take current, skip current)
        - If numbers are not consecutive: dp[i] = dp[i-1] + current points
        
        DP state: dp[i] = max points using numbers up to index i
        """
        # Count frequency of each number
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1

        unique_nums = sorted(freq.keys())
        n = len(unique_nums)
        
        # dp[i+2] represents max points using numbers up to index i
        # +2 offset to handle edge cases easily
        dp = [0] * (n + 2)
        
        for i, val in enumerate(unique_nums):
            points = freq[val] * val  # Total points from this number
            
            # Check if current number is consecutive to previous
            if i != 0 and (unique_nums[i] == unique_nums[i - 1] + 1):
                # Consecutive: can't take both, choose max
                dp[i + 2] = max(dp[i] + points, dp[i + 1])
            else:
                # Not consecutive: safe to take current + all previous
                dp[i + 2] = dp[i + 1] + points
        
        return dp[-1]


# ============================================================================
# SOLUTION 2: SPACE-OPTIMIZED DP (BEST)
# ============================================================================
class Solution2:
    def deleteAndEarn(self, nums: List[int]) -> int:
        """
        Time Complexity: O(n log n) - sorting dominates
        Space Complexity: O(n) - only freq dict and unique_nums (no DP array)
        """
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1

        unique_nums = sorted(freq.keys())
        n = len(unique_nums)
        
        # prev1 = max points from previous position
        # prev2 = max points from two positions back
        prev1, prev2 = 0, 0
        
        for i, val in enumerate(unique_nums):
            points = freq[val] * val
            
            if i != 0 and (unique_nums[i] == unique_nums[i - 1] + 1):
                # Consecutive numbers: max(take current + prev2, skip current)
                current = max(prev2 + points, prev1)
            else:
                # Non-consecutive: safe to take current + all previous
                current = prev1 + points
            
            # Update for next iteration
            prev2 = prev1
            prev1 = current
        
        return prev1


# ============================================================================
# SOLUTION 3: ALTERNATIVE FORMULATION (HOUSE ROBBER STYLE)
# ============================================================================
class Solution3:
    def deleteAndEarn(self, nums: List[int]) -> int:
        """
        Time Complexity: O(max(nums)) - could be large if max value is huge
        Space Complexity: O(max(nums)) - points array
        
        Good when: max(nums) is small and nums has many duplicates
        Bad when: max(nums) is very large (like 10^4) but few unique numbers
        """
        if not nums:
            return 0
        
        max_val = max(nums)
        points = [0] * (max_val + 1)
        
        # Calculate total points for each number
        for num in nums:
            points[num] += num
        
        # Standard House Robber DP
        prev1 = prev2 = 0
        for i in range(1, max_val + 1):
            current = max(prev1, prev2 + points[i])
            prev2 = prev1
            prev1 = current
        
        return prev1


"""
COMPREHENSIVE ANALYSIS:

1. **ALGORITHM UNDERSTANDING**:
   - This is essentially "House Robber" problem in disguise
   - Key insight: if we take number x, we cannot take x-1 or x+1
   - We need to decide: take current number or skip it
   - If numbers are consecutive, we have a choice; if not, we can take both

2. **APPROACH COMPARISON**:

   **Solution 1 (DP Array)**:
   ✅ Clear visualization of DP states
   ✅ Easy to debug and understand
   ❌ Extra O(n) space for DP array
   ❌ Array indexing with offset can be confusing

   **Solution 2 (Space Optimized)**:
   ✅ Optimal space complexity O(1) for DP part
   ✅ Same time complexity
   ✅ Preferred for production code
   ✅ Standard optimization technique

   **Solution 3 (House Robber Style)**:
   ✅ Different perspective, easier for some to understand
   ❌ Can use O(max_val) space which might be huge
   ❌ Inefficient when max(nums) >> unique numbers
"""