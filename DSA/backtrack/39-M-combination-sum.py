# https://leetcode.com/problems/combination-sum/

from typing import List


# =============================================================================
# APPROACH 1: BACKTRACKING WITH INDEX-BASED RECURSION
# =============================================================================

class Solution1:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Index-based backtracking approach with two choices at each step.
        
        Time Complexity: O(N^(T/M)) where N = len(candidates), T = target, M = minimal candidate
        Space Complexity: O(T/M) for recursion stack depth
        
        At each index, we have two choices:
        1. Include current candidate (stay at same index for reuse)
        2. Skip current candidate (move to next index)
        """
        result = []

        def backtrack(idx, remaining, path):
            if remaining == 0:
                result.append(path[:])
                return
            
            # Pruning: invalid states
            if idx >= len(candidates) or remaining < 0:
                return
            
            # Choice 1: Include current candidate (can reuse same index)
            path.append(candidates[idx])
            backtrack(idx, remaining - candidates[idx], path)
            path.pop()  # Backtrack
            
            # Choice 2: Skip current candidate (move to next index)
            backtrack(idx + 1, remaining, path)

        backtrack(0, target, [])
        return result


# =============================================================================
# APPROACH 2: OPTIMIZED BACKTRACKING WITH SORTING
# =============================================================================

class Solution2:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Optimized backtracking with sorting and early pruning.
        
        Time Complexity: O(N^(T/M)) - same worst case but better average case
        Space Complexity: O(T/M) for recursion stack
        """
        result = []
        candidates.sort()  # Enable early pruning
        
        def backtrack(start, remaining, path):
            if remaining == 0:
                result.append(path[:])
                return
            
            # Try each candidate starting from 'start' index
            for i in range(start, len(candidates)):
                # Early pruning: if current candidate > remaining, 
                # all subsequent candidates will also be > remaining
                if candidates[i] > remaining:
                    break
                
                path.append(candidates[i])
                # Recurse with same index 'i' to allow reuse
                backtrack(i, remaining - candidates[i], path)
                # Backtrack
                path.pop()
        
        backtrack(0, target, [])
        return result


# =============================================================================
# APPROACH 3: DYNAMIC PROGRAMMING APPROACH
# =============================================================================

class Solution3:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Dynamic Programming approach building combinations bottom-up.
        
        Time Complexity: O(N * T * average_combinations)
        Space Complexity: O(T * total_combinations)
        
        Build combinations for each target value from 1 to target.
        """
        # dp[i] stores all combinations that sum to i
        dp = [[] for _ in range(target + 1)]
        dp[0] = [[]]  # Base case: one way to make sum 0 (empty combination)
        
        for candidate in candidates:
            for current_sum in range(candidate, target + 1):
                # For each existing combination that sums to (current_sum - candidate),
                # add current candidate to create new combination
                for combination in dp[current_sum - candidate]:
                    dp[current_sum].append(combination + [candidate])
        
        return dp[target]


# =============================================================================
# APPROACH 4: ITERATIVE APPROACH WITH QUEUE
# =============================================================================

class Solution4:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Iterative approach using queue to explore combinations.
        
        Time Complexity: O(N^(T/M)) - same as backtracking
        Space Complexity: O(N^(T/M)) for queue storage
        
        Uses BFS-like approach to build combinations level by level.
        """
        from collections import deque
        
        result = []
        candidates.sort()  # For early pruning
        
        # Queue stores (current_path, remaining_target, start_index)
        queue = deque([([], target, 0)])
        
        while queue:
            path, remaining, start_idx = queue.popleft()
            
            if remaining == 0:
                result.append(path)
                continue
            
            for i in range(start_idx, len(candidates)):
                if candidates[i] > remaining:
                    break  # Early pruning
                
                # Add new state to queue
                new_path = path + [candidates[i]]
                new_remaining = remaining - candidates[i]
                queue.append((new_path, new_remaining, i))
        
        return result


# =============================================================================
# APPROACH 5: MEMOIZED BACKTRACKING
# =============================================================================

class Solution5:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Memoized backtracking to avoid recomputing same subproblems.
        
        Time Complexity: O(N * T) for memoization + combination generation
        Space Complexity: O(N * T) for memoization + recursion stack
        
        Cache results for (start_index, remaining_target) pairs.
        """
        from functools import lru_cache
        
        candidates.sort()
        
        @lru_cache(maxsize=None)
        def backtrack(start, remaining):
            if remaining == 0:
                return [[]]
            
            result = []
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                
                # Get all combinations for remaining target
                sub_combinations = backtrack(i, remaining - candidates[i])
                
                # Add current candidate to each sub-combination
                for combo in sub_combinations:
                    result.append([candidates[i]] + combo)
            
            return result
        
        return backtrack(0, target)

# =============================================================================
# COMPLEXITY ANALYSIS & COMPARISON
# =============================================================================

"""
COMPLEXITY ANALYSIS:

Time Complexity: O(N^(T/M)) where:
- N = number of candidates
- T = target value  
- M = minimal candidate value
- In worst case, we might need to explore all possible combinations

Space Complexity: O(T/M) for recursion stack depth

DETAILED ANALYSIS:
- The recursion depth is at most T/M (when we use the smallest candidate repeatedly)
- At each level, we might branch into N different paths
- Total combinations can be exponential in worst case

APPROACH COMPARISON:

1. Index-based Backtracking:
   ✅ Clear logic with include/exclude choices
   ✅ Easy to understand and debug
   ❌ Slightly more recursive calls

2. Optimized Backtracking (RECOMMENDED):
   ✅ Best balance of readability and performance
   ✅ Early pruning with sorted candidates
   ✅ Efficient for-loop structure
   ✅ Industry standard approach

3. Dynamic Programming:
   ✅ Avoids redundant computations
   ❌ Higher space complexity
   ❌ Less intuitive for this problem

4. Iterative with Queue:
   ✅ No recursion stack overflow risk
   ✅ Easy to understand flow
   ❌ Higher memory usage for queue

5. Memoized Backtracking:
   ✅ Optimal for repeated subproblems
   ❌ Overhead of memoization
   ❌ Complex result combination


OPTIMIZATION TECHNIQUES:

1. Sorting: Enables early pruning when candidate > remaining
2. Early Termination: Break loop when impossible to find solution
3. Path Management: Use list append/pop instead of creating new lists
4. Start Index: Prevent duplicate combinations by maintaining order

INTERVIEW TIPS:
- Start with Approach 2 (Optimized Backtracking)
- Explain the sorting optimization
- Mention the early pruning benefit
- Discuss time/space complexity clearly
- Show how to avoid duplicates with start index
"""
