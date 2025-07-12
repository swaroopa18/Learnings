from typing import List

# =============================================================================
# SOLUTION 1: ITERATIVE APPROACH (Building permutations incrementally)
# =============================================================================

class Solution1:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Iterative approach: Build permutations by inserting each number 
        at all possible positions in existing permutations.
        """
        output = [[]]  # Start with one empty permutation
        
        for num in nums:
            newOp = []
            # For each existing permutation
            for perm in output:
                # Insert current number at every possible position
                for i in range(len(perm) + 1):
                    # Create new permutation with num inserted at position i
                    newOp.append(perm[:i] + [num] + perm[i:])
            output = newOp[:]  # Replace old permutations with new ones
        
        return output

# Time Complexity: O(n! * n)
# - We generate n! permutations
# - For each permutation, we do O(n) work to create it (slicing and concatenation)
# 
# Space Complexity: O(n! * n) 
# - We store n! permutations, each of length n
# - Additional O(n! * n) for intermediate newOp lists

# =============================================================================
# SOLUTION 2: BACKTRACKING APPROACH (Depth-First Search)
# =============================================================================

class Solution2:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Backtracking approach: Use DFS to build permutations by making choices
        and undoing them (backtracking).
        
        Algorithm:
        1. Maintain current permutation and visited array
        2. At each step, try adding each unused number
        3. Recurse with updated state
        4. Backtrack by removing the choice and marking as unused
        
        This explores the decision tree systematically.
        """
        n = len(nums)
        result = []

        def backtrack(curr, visited):
            if len(curr) == n:
                result.append(curr[:])  # Add copy of current permutation
                return
            
            for i in range(n):
                if visited[i] == 0:  # If number not used
                    # Make choice
                    curr.append(nums[i])
                    visited[i] = 1
                    
                    # Recurse
                    backtrack(curr, visited)
                    
                    # Backtrack (undo choice)
                    curr.pop()
                    visited[i] = 0

        backtrack([], [0] * n)
        return result

# Time Complexity: O(n! * n)
# - We explore n! permutations
# - For each complete permutation, we do O(n) work to copy it
# - The recursive calls form a tree with n! leaves
#
# Space Complexity: O(n! * n + n)
# - O(n! * n) for storing all permutations
# - O(n) for recursion stack depth
# - O(n) for visited array and current permutation

# =============================================================================
# SOLUTION 3: OPTIMIZED BACKTRACKING (Swap-based)
# =============================================================================

class Solution3:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Optimized backtracking: Instead of maintaining visited array,
        swap elements to generate permutations in-place.
        
        Algorithm:
        1. For each position, try placing each remaining element
        2. Swap current element with chosen element
        3. Recurse for next position
        4. Swap back to restore original state
        
        This is more space-efficient as it doesn't need visited array.
        """
        result = []
        
        def backtrack(start):
            # Base case: all positions filled
            if start == len(nums):
                result.append(nums[:])  # Add copy of current permutation
                return
            
            # Try each element for current position
            for i in range(start, len(nums)):
                # Swap current element with chosen element
                nums[start], nums[i] = nums[i], nums[start]
                
                # Recurse for next position
                backtrack(start + 1)
                
                # Backtrack (swap back)
                nums[start], nums[i] = nums[i], nums[start]
        
        backtrack(0)
        return result

# Time Complexity: O(n! * n) - same as above
# Space Complexity: O(n! * n + n) - but uses less auxiliary space

# =============================================================================
# SOLUTION 4: USING BUILT-IN LIBRARY (Most Practical)
# =============================================================================

from itertools import permutations

class Solution4:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Using Python's built-in permutations function.
        Most practical for real-world use.
        """
        return [list(perm) for perm in permutations(nums)]

# Time Complexity: O(n! * n)
# Space Complexity: O(n! * n)
