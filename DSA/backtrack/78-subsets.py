from typing import List

# APPROACH 1: ITERATIVE (Bottom-up Dynamic Programming)
# Time Complexity: O(2^n) - We generate all 2^n subsets
# Space Complexity: O(2^n) - To store all subsets in output
# 
# REASONING: Start with empty subset, then for each number, create new subsets
# by adding the current number to all existing subsets
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        output = [[]]
        
        for num in nums:
            newsets = []
            # For each existing subset, create a new subset by adding current number
            for subset in output:
                newsets.append(subset + [num])  # Create new subset with current number
            output.extend(newsets)
        return output

# APPROACH 2: RECURSIVE BACKTRACKING (DFS)
# Time Complexity: O(2^n) - We explore all 2^n possibilities
# Space Complexity: O(n) - Recursion depth is n, plus O(2^n) for storing results
#
# REASONING: At each position, we have 2 choices - include or exclude the element
# This naturally forms a binary decision tree of height n
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []

        def backtrack(idx, path):
            if idx >= len(nums):
                result.append(path[:])  # Add copy of current path to result
                return
            
            # Choice 1: Include current element
            path.append(nums[idx])
            backtrack(idx + 1, path)
            
            # Choice 2: Exclude current element (backtrack)
            path.pop()  # Remove the element we just added
            backtrack(idx + 1, path)

        backtrack(0, [])
        return result

# APPROACH 3: BIT MANIPULATION (Most Efficient)
# Time Complexity: O(n * 2^n) - Generate 2^n subsets, each taking O(n) time
# Space Complexity: O(1) - Only using constant extra space (excluding output)
#
# REASONING: Each subset corresponds to a binary number from 0 to 2^n-1
# If bit i is set in the number, include nums[i] in the subset
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        n = len(nums)
        
        # Generate all numbers from 0 to 2^n - 1
        for i in range(2**n):
            subset = []
            # Check each bit position
            for j in range(n):
                # If j-th bit is set, include nums[j]
                if i & (1 << j):
                    subset.append(nums[j])
            result.append(subset)
        
        return result

# APPROACH 4: CLEANER BACKTRACKING (Include at each level)
# Time Complexity: O(2^n) - Same as approach 2
# Space Complexity: O(n) - Recursion depth
#
# REASONING: Instead of deciding include/exclude at each element,
# we add current state to result at each level and explore further
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        
        def backtrack(start, path):
            # Add current subset to result
            result.append(path[:])
            
            # Try adding each remaining element
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)  # Move to next position
                path.pop()  # Backtrack
        
        backtrack(0, [])
        return result

"""
COMPARISON OF APPROACHES:

1. ITERATIVE (Approach 1):
   - Pros: Easy to understand, no recursion overhead
   - Cons: Creates many intermediate lists, higher memory usage
   - Best for: When you want to avoid recursion

2. RECURSIVE BACKTRACKING (Approach 2):
   - Pros: Clean recursive structure, follows problem's nature
   - Cons: Recursion overhead, can be confusing for beginners
   - Best for: When you want to understand the decision tree

3. BIT MANIPULATION (Approach 3):
   - Pros: Most space-efficient, leverages binary representation
   - Cons: Less intuitive, harder to debug
   - Best for: When memory is critical, or for educational purposes

4. CLEANER BACKTRACKING (Approach 4):
   - Pros: Most intuitive, follows standard backtracking template
   - Cons: Slight overhead in copying path at each level
   - Best for: General backtracking practice, most readable

RECOMMENDATION:
- For interviews: Use Approach 4 (cleaner backtracking) - it's most intuitive
- For production: Use Approach 3 (bit manipulation) - it's most efficient
- For learning: Start with Approach 1, then move to Approach 4
"""