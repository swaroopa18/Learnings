# https://leetcode.com/problems/combination-sum-ii/description/

from typing import List


# =============================================================================
# APPROACH 1: BRUTE FORCE WITH SET (Your First Solution)
# =============================================================================

class Solution1:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Brute force approach using set to eliminate duplicate combinations.
        
        Time Complexity: O(2^N * N) where N = len(candidates)
        Space Complexity: O(2^N * N) for storing combinations in set
        
        Problems with this approach:
        - Inefficient: generates duplicates then removes them
        - High memory usage due to set storage
        - Sorting each combination is expensive
        - Not optimal for interviews
        """
        result = []
        combos = set()  # Store tuples of sorted combinations to detect duplicates

        def backtrack(start, remaining, path):
            if remaining == 0:
                # Sort the path to create canonical representation
                combo = tuple(sorted(path[:]))
                if combo not in combos:
                    result.append(path[:])
                    combos.add(combo)
                return
            
            for i in range(start, len(candidates)):
                if candidates[i] <= remaining:
                    path.append(candidates[i])
                    # Use i+1 to ensure each element is used only once
                    backtrack(i + 1, remaining - candidates[i], path)
                    path.pop()
                else:
                    # Even if current candidate is too large, try next one
                    # This is inefficient without sorting
                    backtrack(i + 1, remaining, path)

        backtrack(0, target, [])
        return result


# =============================================================================
# APPROACH 2: OPTIMIZED BRUTE FORCE WITH SORTING (Your Second Solution)
# =============================================================================

class Solution2:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Improved brute force with sorting for early pruning.
        
        Time Complexity: O(2^N * N) - still generates duplicates
        Space Complexity: O(2^N * N) for set storage
        
        Improvements over Approach 1:
        - Sorting enables early pruning (break when candidate > remaining)
        - Reduces unnecessary recursive calls
        - Still uses set for duplicate elimination (not optimal)
        """
        result = []
        candidates.sort()  # Enable early pruning
        combos = set()

        def backtrack(start, remaining, path):
            if remaining == 0:
                combo = tuple(sorted(path[:]))  # Still need to sort for deduplication
                if combo not in combos:
                    result.append(path[:])
                    combos.add(combo)
                return
            
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break  # Early pruning: no need to check further candidates
                
                path.append(candidates[i])
                backtrack(i + 1, remaining - candidates[i], path)
                path.pop()

        backtrack(0, target, [])
        return result


# =============================================================================
# APPROACH 3: OPTIMAL SOLUTION WITH DUPLICATE SKIPPING (Your Third Solution - BROKEN)
# =============================================================================

class Solution3_Broken:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        BROKEN IMPLEMENTATION - Shows common mistake in duplicate handling.
        
        The bug: path.append() and path.pop() are outside the condition check.
        This means we always add and remove the element, but only recurse conditionally.
        This leads to incorrect path building and wrong results.
        """
        result = []
        candidates.sort()

        def backtrack(start, remaining, path):
            if remaining == 0:
                result.append(path[:])
                return
            
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                
                if i == start or candidates[i] != candidates[i - 1]:
                    path.append(candidates[i])
                    backtrack(i + 1, remaining - candidates[i], path)
                    path.pop()

        backtrack(0, target, [])
        return result

# =============================================================================
# APPROACH 5: ALTERNATIVE DUPLICATE HANDLING WITH USAGE TRACKING
# =============================================================================

class Solution5:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Alternative approach using usage tracking for duplicate handling.
        
        Time Complexity: O(2^N)
        Space Complexity: O(N) for recursion stack + usage array
        
        Instead of skipping duplicates, track which elements are used.
        """
        result = []
        candidates.sort()
        used = [False] * len(candidates)

        def backtrack(start, remaining, path):
            if remaining == 0:
                result.append(path[:])
                return
            
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                
                # Skip if already used or if it's a duplicate and previous duplicate not used
                if used[i] or (i > 0 and candidates[i] == candidates[i - 1] and not used[i - 1]):
                    continue
                
                used[i] = True
                path.append(candidates[i])
                backtrack(i + 1, remaining - candidates[i], path)
                path.pop()
                used[i] = False

        backtrack(0, target, [])
        return result



# =============================================================================
# COMPLEXITY ANALYSIS & COMPARISON
# =============================================================================

"""
COMPLEXITY ANALYSIS:

Time Complexity: O(2^N) in worst case where N = len(candidates)
- Each element can be included or excluded
- With duplicate handling, actual complexity is much better in practice

Space Complexity: O(N) for recursion stack depth
- Maximum recursion depth is N (when we include all candidates)
- Additional space for result storage

APPROACH COMPARISON:

1. Brute Force with Set:
   ❌ Inefficient: O(2^N * N) time due to sorting in set
   ❌ High memory usage for set storage
   ❌ Not suitable for interviews

2. Optimized Brute Force:
   ✅ Better than #1 due to early pruning
   ❌ Still uses set for deduplication
   ❌ Still sorts each combination

3. Broken Implementation:
   ❌ Shows common mistake in backtracking
   ❌ Incorrect path management
   ❌ Educational value only

4. Optimal Solution (RECOMMENDED):
   ✅ Prevents duplicates during generation
   ✅ No extra space for deduplication
   ✅ Clean and efficient
   ✅ Industry standard approach

5. Usage Tracking:
   ✅ Clear logic for duplicate handling
   ✅ Easy to understand and debug
   ❌ Extra space for usage array

6. Frequency-Based:
   ✅ Systematic approach to duplicates
   ✅ Good for understanding the problem
   ❌ More complex implementation
   ❌ Harder to code in interview setting

KEY INSIGHTS:

1. **Duplicate Handling Strategy:**
   - Sort the array first
   - Skip duplicates at the same recursion level
   - Use condition: `i > start and candidates[i] == candidates[i-1]`

2. **Why Sorting is Critical:**
   - Groups duplicate elements together
   - Enables the duplicate skipping logic
   - Allows early pruning when candidate > remaining

3. **Common Mistakes:**
   - Not handling duplicates properly
   - Using set for deduplication (inefficient)
   - Incorrect path management in backtracking
   - Wrong condition for duplicate skipping

4. **Interview Strategy:**
   - Start with Approach 4 (Optimal Solution)
   - Explain the duplicate skipping logic clearly
   - Walk through example with duplicates
   - Discuss why sorting is necessary
   - Mention the time/space complexity

DUPLICATE SKIPPING EXPLANATION:
When we have duplicates like [1, 1, 2] and we're at the same recursion level:
- First 1: Always consider (i == start)
- Second 1: Skip if it's at the same level (i > start and candidates[i] == candidates[i-1])
- This ensures we don't generate duplicate combinations like [1,2] twice

The key insight is that we only skip duplicates at the SAME recursion level,
not across different levels. This allows us to use multiple instances of the
same number (like [1,1,6]) while avoiding duplicate combinations.
"""


# =============================================================================
# EXAMPLE WALKTHROUGH
# =============================================================================

"""
EXAMPLE WALKTHROUGH:
candidates = [10,1,2,7,6,1,5], target = 8

Step 1: Sort candidates = [1,1,2,5,6,7,10]

Step 2: Backtrack with duplicate skipping:

backtrack(0, 8, []):
├── Try candidates[0] = 1: path = [1]
│   ├── backtrack(1, 7, [1]):
│   │   ├── Skip candidates[1] = 1 (duplicate at same level)
│   │   ├── Try candidates[2] = 2: path = [1,2]
│   │   │   └── backtrack(3, 5, [1,2]):
│   │   │       └── Try candidates[3] = 5: path = [1,2,5]
│   │   │           └── backtrack(4, 0, [1,2,5]): ✅ Add [1,2,5]
│   │   └── Try candidates[4] = 6: path = [1,6]
│   │       └── backtrack(5, 1, [1,6]): remaining < 7, no solution
│   └── Try candidates[1] = 1: path = [1] (different level, allowed)
│       └── backtrack(2, 6, [1,1]):
│           └── Try candidates[4] = 6: path = [1,1,6]
│               └── backtrack(5, 0, [1,1,6]): ✅ Add [1,1,6]
├── Try candidates[2] = 2: path = [2]
│   └── backtrack(3, 6, [2]):
│       └── Try candidates[4] = 6: path = [2,6]
│           └── backtrack(5, 0, [2,6]): ✅ Add [2,6]
└── Try candidates[5] = 7: path = [7]
    └── backtrack(6, 1, [7]): remaining < 10, no solution

Final result: [[1,2,5], [1,1,6], [2,6], [7]]
"""