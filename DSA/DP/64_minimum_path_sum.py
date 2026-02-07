from typing import List


class Solution:
    """
    Problem: Minimum Path Sum
    Given a m x n grid filled with non-negative numbers, find a path from top left 
    to bottom right which minimizes the sum of all numbers along its path.
    Note: You can only move either down or right at any point in time.
    """
    
    # ========================================================================
    # APPROACH 1: Recursion (Brute Force) - NOT RECOMMENDED
    # Time Complexity: O(2^(m+n)) - exponential, explores all paths
    # Space Complexity: O(m+n) - recursion stack depth
    # ========================================================================
    def minPathSum_recursion(self, grid: List[List[int]]) -> int:
        """
        Basic recursive solution - explores all possible paths.
        Very inefficient due to repeated subproblems.
        """
        m, n = len(grid), len(grid[0])
        
        def dfs(i: int, j: int) -> int:
            # Base case: reached destination
            if i == m - 1 and j == n - 1:
                return grid[i][j]
            
            # Out of bounds
            if i >= m or j >= n:
                return float('inf')
            
            # Explore both paths: down and right
            down = dfs(i + 1, j)
            right = dfs(i, j + 1)
            
            # Current cell + minimum of two paths
            return grid[i][j] + min(down, right)
        
        return dfs(0, 0)
    
    # ========================================================================
    # APPROACH 2: Recursion with Memoization (Top-Down DP)
    # Time Complexity: O(m*n) - each cell computed once
    # Space Complexity: O(m*n) - memo table + O(m+n) recursion stack
    # ========================================================================
    def minPathSum_memoization(self, grid: List[List[int]]) -> int:
        """
        Top-down DP using memoization to cache computed results.
        Solves the repeated subproblem issue from pure recursion.
        """
        m, n = len(grid), len(grid[0])
        memo = {}  # Dictionary to store computed results
        
        def dfs(i: int, j: int) -> int:
            # Base case: reached destination
            if i == m - 1 and j == n - 1:
                return grid[i][j]
            
            # Out of bounds
            if i >= m or j >= n:
                return float('inf')
            
            # Check if already computed
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Compute and store result
            down = dfs(i + 1, j)
            right = dfs(i, j + 1)
            memo[(i, j)] = grid[i][j] + min(down, right)
            
            return memo[(i, j)]
        
        return dfs(0, 0)
    
    # ========================================================================
    # APPROACH 3: Dynamic Programming (Bottom-Up) - 2D Array
    # Time Complexity: O(m*n) - iterate through all cells once
    # Space Complexity: O(m*n) - 2D DP table
    # ========================================================================
    def minPathSum(self, grid: List[List[int]]) -> int:
        """
        Bottom-up DP solution (YOUR ORIGINAL APPROACH).
        Build solution iteratively from top-left to bottom-right.
        This is more intuitive and avoids recursion overhead.
        """
        m, n = len(grid), len(grid[0])
        dp = [[0 for _ in range(n)] for _ in range(m)]

        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    # Starting point
                    dp[0][0] = grid[0][0]
                elif i == 0:
                    # First row: can only come from left
                    dp[0][j] = grid[0][j] + dp[0][j - 1]
                elif j == 0:
                    # First column: can only come from above
                    dp[i][0] = grid[i][0] + dp[i - 1][0]
                else:
                    # Can come from either above or left, choose minimum
                    dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
        
        return dp[m - 1][n - 1]
    
    # ========================================================================
    # APPROACH 4: Space-Optimized DP - 1D Array (Rolling Array)
    # Time Complexity: O(m*n) - still iterate through all cells
    # Space Complexity: O(n) - only need one row at a time
    # ========================================================================
    def minPathSum_optimized_1d(self, grid: List[List[int]]) -> int:
        """
        Space-optimized version using only 1D array.
        Since we only need the previous row and current row values,
        we can reduce space from O(m*n) to O(n).
        """
        m, n = len(grid), len(grid[0])
        dp = [0] * n
        
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    dp[j] = grid[0][0]
                elif i == 0:
                    dp[j] = grid[0][j] + dp[j - 1]
                elif j == 0:
                    dp[j] = grid[i][0] + dp[j]  # dp[j] has previous row's value
                else:
                    # dp[j] = value from above (previous iteration)
                    # dp[j-1] = value from left (current iteration)
                    dp[j] = grid[i][j] + min(dp[j], dp[j - 1])
        
        return dp[n - 1]
    
    # ========================================================================
    # APPROACH 5: In-Place Modification (Most Space Efficient)
    # Time Complexity: O(m*n)
    # Space Complexity: O(1) - modify input grid directly
    # NOTE: This modifies the input, which may not be acceptable in all cases
    # ========================================================================
    def minPathSum_inplace(self, grid: List[List[int]]) -> int:
        """
        Most space-efficient solution - modifies input grid.
        Only use if modifying input is acceptable.
        """
        m, n = len(grid), len(grid[0])
        
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue  # Starting point stays same
                elif i == 0:
                    grid[0][j] += grid[0][j - 1]
                elif j == 0:
                    grid[i][0] += grid[i - 1][0]
                else:
                    grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])
        
        return grid[m - 1][n - 1]


# ============================================================================
# COMPARISON SUMMARY
# ============================================================================
"""
┌──────────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Approach             │ Time Complexity │ Space Complexity│ Notes           │
├──────────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ 1. Pure Recursion    │ O(2^(m+n))      │ O(m+n)          │ Too slow, avoid │
│ 2. Memoization       │ O(m*n)          │ O(m*n) + stack  │ Good for learning│
│ 3. 2D DP (Original)  │ O(m*n)          │ O(m*n)          │ Clear & standard│
│ 4. 1D DP Array       │ O(m*n)          │ O(n)            │ Space optimized │
│ 5. In-place          │ O(m*n)          │ O(1)            │ Best space, but │
│                      │                 │                 │ modifies input  │
└──────────────────────┴─────────────────┴─────────────────┴─────────────────┘

RECOMMENDATION:
- For interviews: Use Approach 3 (2D DP) - it's clear and easy to explain
- For production with space constraints: Use Approach 4 (1D array)
- If input can be modified: Use Approach 5 (in-place)
- Understand Approach 2 (memoization) for top-down DP pattern practice

KEY INSIGHT:
Each cell's minimum path sum = current cell value + min(path from above, path from left)
This overlapping subproblem structure makes it perfect for DP!
"""