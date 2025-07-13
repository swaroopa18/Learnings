from typing import List

# ============================================================================
# PROBLEM: Next Permutation - Multiple Approaches Analysis
# ============================================================================
# Find the next lexicographically greater permutation of numbers.
# If no such permutation exists, return the lexicographically smallest.
# ============================================================================

class Solution1_BruteForce:
    """
    BRUTE FORCE APPROACH - Generate all permutations
    
    Time Complexity: O(n! × n) - Exponential, extremely inefficient
    Space Complexity: O(n! × n) - Stores all permutations
    
    MAJOR ISSUES:
    1. Exponential time complexity - unusable for n > 8
    2. Massive memory usage
    3. Unnecessary computation of all permutations
    4. Code has bugs in expected_perm logic
    """
    def permute(self, nums):
        n = len(nums)
        result = []

        def backtrack(curr, visited):
            if len(curr) == n:
                result.append(curr[:])  # O(n) copy operation
            for i in range(len(nums)):
                if not visited[i]:
                    curr.append(nums[i])
                    visited[i] = True
                    backtrack(curr, visited)  # Recursive call
                    curr.pop()
                    visited[i] = False

        backtrack([], [False] * n)
        return result

    def nextPermutation(self, nums: List[int]) -> None:
        sorted_nums = sorted(nums)  # O(n log n)
        permutations = self.permute(sorted_nums)  # O(n!)
        expected_perm = []
        
        # BUG: This logic is flawed and overcomplicated
        for i, perm in enumerate(permutations):
            if tuple(perm) == tuple(nums):
                expected_perm.append(
                    permutations[0]
                    if i == len(permutations) - 1
                    else permutations[i + 1]
                )

        # BUG: expected_perm[-1] assumes list is not empty
        for i in range(len(expected_perm[-1])):
            nums[i] = expected_perm[-1][i]


class Solution2_Inefficient:
    """
    INEFFICIENT APPROACH - Buggy implementation
    
    Time Complexity: O(n²) worst case due to nested loops
    Space Complexity: O(n) due to sorted() creating new array
    
    ISSUES:
    1. Variable 'r' not reset properly in outer loop
    2. Uses sorted() instead of in-place reversal
    3. Inefficient nested loop structure
    4. Creates unnecessary temporary arrays
    """
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)
        l, r = n - 1, n - 1
        while l != 0:
            if nums[l] > nums[l - 1]:
                while r >= l:  # BUG: r not reset for each iteration
                    if nums[l - 1] < nums[r]:
                        nums[l - 1], nums[r] = nums[r], nums[l - 1]
                        break
                    else:
                        r -= 1
                # INEFFICIENT: O(n log n) + O(n) space
                sorted_nums = sorted(nums[l:])
                for i in range(l, n):
                    nums[i] = sorted_nums[i - l]
                return
            else:
                l -= 1
        nums.sort()  # O(n log n)


class Solution3_Optimal:
    """
    OPTIMAL APPROACH - Standard algorithm
    
    Time Complexity: O(n) - Linear scan
    Space Complexity: O(1) - Constant extra space
    
    This is the standard, most efficient solution.
    """
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)
        l = n - 2
        
        # Step 1: Find the first decreasing element from the right
        while l >= 0 and nums[l] >= nums[l + 1]:
            l -= 1

        if l >= 0:
            r = n - 1
            # Step 2: Find the element just larger than nums[l]
            while nums[r] <= nums[l]:
                r -= 1
            nums[l], nums[r] = nums[r], nums[l]

        # Step 3: Reverse the suffix
        nums[l + 1:] = reversed(nums[l + 1:])


class Solution5_BinarySearch:
    """
    OPTIMIZED FOR LARGE ARRAYS - Uses binary search
    
    Time Complexity: O(n) average, O(n + log n) for step 2
    Space Complexity: O(1)
    
    Useful when the array is very large and the suffix is long.
    In practice, rarely needed as linear search is fast enough.
    """
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)
        
        # Step 1: Find pivot
        pivot = -1
        for i in range(n - 2, -1, -1):
            if nums[i] < nums[i + 1]:
                pivot = i
                break
        
        if pivot == -1:
            nums.reverse()
            return
        
        # Step 2: Binary search for successor
        left, right = pivot + 1, n - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > nums[pivot]:
                left = mid + 1
            else:
                right = mid - 1
        
        # Swap with the rightmost element > pivot
        nums[pivot], nums[right] = nums[right], nums[pivot]
        
        # Step 3: Reverse suffix
        self.reverse(nums, pivot + 1, n - 1)
    
    def reverse(self, nums: List[int], left: int, right: int) -> None:
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1


class Solution6_Iterative:
    """
    ITERATIVE APPROACH - No recursion
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Alternative implementation focusing on iterative logic.
    """
    def nextPermutation(self, nums: List[int]) -> None:
        def find_pivot():
            for i in range(len(nums) - 2, -1, -1):
                if nums[i] < nums[i + 1]:
                    return i
            return -1
        
        def find_successor(pivot):
            for i in range(len(nums) - 1, pivot, -1):
                if nums[i] > nums[pivot]:
                    return i
            return -1
        
        pivot = find_pivot()
        
        if pivot == -1:
            nums.reverse()
        else:
            successor = find_successor(pivot)
            nums[pivot], nums[successor] = nums[successor], nums[pivot]
            nums[pivot + 1:] = reversed(nums[pivot + 1:])


# ============================================================================
# COMPLEXITY ANALYSIS & COMPARISON
# ============================================================================

def complexity_analysis():
    """
    DETAILED COMPLEXITY COMPARISON:
    
    ┌─────────────────┬─────────────┬─────────────┬─────────────────────────────┐
    │    Solution     │ Time Comp.  │ Space Comp. │           Notes             │
    ├─────────────────┼─────────────┼─────────────┼─────────────────────────────┤
    │ Solution1       │ O(n! × n)   │ O(n! × n)   │ Exponential - AVOID!        │
    │ Solution2       │ O(n²)       │ O(n)        │ Buggy and inefficient       │
    │ Solution3       │ O(n)        │ O(1)        │ Optimal - RECOMMENDED       │
    │ Solution5       │ O(n+log n)  │ O(1)        │ Over-optimization           │
    │ Solution6       │ O(n)        │ O(1)        │ Clean iterative approach    │
    └─────────────────┴─────────────┴─────────────┴─────────────────────────────┘
    
    PERFORMANCE FOR DIFFERENT INPUT SIZES:
    
    n=3:  All O(n) solutions perform similarly
    n=8:  Solution1 takes ~40,000x longer than optimal
    n=10: Solution1 becomes unusable (3.6M permutations)
    n=12: Solution1 would take hours to complete
    
    MEMORY USAGE:
    - Solution1: Stores all n! permutations
    - Solution2: Creates temporary sorted arrays
    - Solutions 3-6: Only use a few variables
    """
    pass


# ============================================================================
# STEP-BY-STEP ALGORITHM EXPLANATION
# ============================================================================

def algorithm_walkthrough():
    """
    THE OPTIMAL ALGORITHM EXPLAINED:
    
    INTUITION:
    - We want the next lexicographically larger permutation
    - Find the rightmost position where we can increase a digit
    - Make the smallest possible increase at that position
    - Arrange the rest in smallest possible order
    
    STEPS:
    1. FIND PIVOT: Scan from right, find first nums[i] < nums[i+1]
       - This is the rightmost position we can increase
       - If no such position exists, we have the last permutation
    
    2. FIND SUCCESSOR: From right side, find smallest element > pivot
       - This gives us the smallest possible increase
       - Due to descending order, first element > pivot is the answer
    
    3. SWAP: Exchange pivot with its successor
       - Now we have increased the permutation
    
    4. REVERSE SUFFIX: Reverse everything after pivot position
       - Suffix is in descending order after swap
       - We want ascending order for lexicographically smallest
    
    EXAMPLE: [1, 2, 7, 4, 3, 1]
    
    Step 1: Find pivot
    - 1 < 3? No
    - 3 < 4? No  
    - 4 < 7? No
    - 7 < 2? No
    - 2 < 1? No
    - 1 < 2? Yes! Pivot = 0, nums[0] = 1
    
    Step 2: Find successor
    - From right: 1 > 1? No
    - 3 > 1? Yes! Successor = 4, nums[4] = 3
    
    Step 3: Swap
    - [1, 2, 7, 4, 3, 1] → [3, 2, 7, 4, 1, 1]
    
    Step 4: Reverse suffix
    - Reverse [2, 7, 4, 1, 1] → [1, 1, 4, 7, 2]
    - Final: [3, 1, 1, 4, 7, 2]
    """
    pass


# ============================================================================
# COMMON MISTAKES & BEST PRACTICES
# ============================================================================

"""
    COMMON MISTAKES TO AVOID:
    
    1. GENERATING ALL PERMUTATIONS:
       ❌ Don't use backtracking/recursion to generate all permutations
       ✅ Use the direct O(n) algorithm
    
    2. USING SORTING INSTEAD OF REVERSAL:
       ❌ sorted_nums = sorted(nums[l:])
       ✅ nums[l+1:] = reversed(nums[l+1:])
    
    3. NOT HANDLING EDGE CASES:
       ❌ Forgetting the last permutation case
       ✅ Always check if pivot exists, reverse entire array if not
    
    4. INDEX ERRORS:
       ❌ Starting from wrong position or off-by-one errors
       ✅ Carefully handle boundary conditions
    
    5. INEFFICIENT SUCCESSOR SEARCH:
       ❌ Using nested loops or complex logic
       ✅ Simple linear scan from right
    
    6. MEMORY OVERHEAD:
       ❌ Creating temporary arrays unnecessarily
       ✅ Modify input array in-place
    
    BEST PRACTICES:
    1. Always use the O(n) algorithm
    
"""