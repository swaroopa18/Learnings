from typing import List


class Solution:
    """
    Problem: Subarray Sum Equals K
    Given an array of integers and an integer k, find the total number of 
    continuous subarrays whose sum equals k.
    """
    
    # ============================================================================
    # APPROACH 1: Brute Force - Two Nested Loops
    # ============================================================================
    # Time Complexity: O(n²) - two nested loops
    # Space Complexity: O(1) - only using constant extra space
    # 
    # How it works:
    # - For each starting position i, calculate sum of all subarrays starting at i
    # - Check if any of these sums equals k
    # - Count all matches
    #
    # Pros: Simple to understand, no extra space needed
    # Cons: Slow for large inputs
    # ============================================================================
    def subarraySum_bruteforce(self, nums: List[int], k: int) -> int:
        count = 0
        
        # Try every possible starting position
        for i in range(len(nums)):
            total = 0
            
            # Extend subarray from position i
            for j in range(i, len(nums)):
                total += nums[j]  # Add current element to running sum
                
                if total == k:
                    count += 1
                    
        return count


    # ============================================================================
    # APPROACH 2: Prefix Sum with Hash Map (OPTIMAL)
    # ============================================================================
    # Time Complexity: O(n) - single pass through array
    # Space Complexity: O(n) - hash map can store up to n prefix sums
    #
    # Key Insight:
    # If we know the cumulative sum up to index i is "total", and we want 
    # subarrays ending at i that sum to k, we need to find how many times 
    # we've seen cumulative sum = (total - k) before index i.
    #
    # Why? Because: cumulative_sum[j] - cumulative_sum[i] = k
    #              => cumulative_sum[i] = cumulative_sum[j] - k
    #
    # Example: nums = [1, 2, 3], k = 3
    # Index 0: total=1, looking for (1-3)=-2, count=0
    # Index 1: total=3, looking for (3-3)=0, count=1 (found one!)
    # Index 2: total=6, looking for (6-3)=3, count=1 (the prefix sum 3 exists!)
    # Total subarrays: 2  ([3] and [1,2])
    #
    # Pros: Optimal time complexity, handles negative numbers
    # Cons: Uses extra space for hash map
    # ============================================================================
    def subarraySum(self, nums: List[int], k: int) -> int:
        total_count = 0
        
        # Hash map: {prefix_sum: frequency}
        # Initialize with {0: 1} because an empty prefix has sum 0
        # This handles cases where subarray starts from index 0
        prefix_sums = {0: 1}
        
        total = 0  # Running cumulative sum
        
        for num in nums:
            total += num  # Update cumulative sum
            
            # Check if (total - k) exists in our prefix sums
            # If yes, we found subarray(s) that sum to k
            key = total - k
            if key in prefix_sums:
                total_count += prefix_sums[key]
            
            # Add current cumulative sum to hash map
            prefix_sums[total] = prefix_sums.get(total, 0) + 1
            
        return total_count


# ============================================================================
# EXAMPLE WALKTHROUGH
# ============================================================================
# Input: nums = [1, 1, 1], k = 2
#
# Brute Force:
# i=0: [1]=1, [1,1]=2✓, [1,1,1]=3 → count=1
# i=1: [1]=1, [1,1]=2✓ → count=2
# i=2: [1]=1 → count=2
#
# Hash Map Approach:
# Initial: prefix_sums = {0: 1}, total = 0, count = 0
# 
# i=0, num=1: total=1, key=1-2=-1 (not found), prefix_sums={0:1, 1:1}
# i=1, num=1: total=2, key=2-2=0 (found! count+=1), prefix_sums={0:1, 1:1, 2:1}
# i=2, num=1: total=3, key=3-2=1 (found! count+=1), prefix_sums={0:1, 1:1, 2:1, 3:1}
# 
# Final count = 2 ✓
# ============================================================================


# ============================================================================
# COMPLEXITY COMPARISON
# ============================================================================
#
# Approach          | Time    | Space | Best for
# ------------------|---------|-------|----------------------------------
# Brute Force       | O(n²)   | O(1)  | Very small inputs, interviews
# Prefix Sum HashMap| O(n)    | O(n)  | Production code (OPTIMAL)
#
# Recommendation: Use the hash map approach for optimal performance
# ============================================================================