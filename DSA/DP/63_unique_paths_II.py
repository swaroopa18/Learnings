from typing import List


class Solution:
    """
    Problem: Unique Paths II (With Obstacles)
    
    A robot is located at the top-left corner of a m x n grid.
    The robot can only move either down or right at any point in time.
    The robot is trying to reach the bottom-right corner of the grid.
    
    Now consider if some obstacles are added to the grids. 
    How many unique paths would there be?
    
    An obstacle and space is marked as 1 and 0 respectively in the grid.
    """
    
    # ========================================================================
    # APPROACH 1: Recursion (Brute Force) - NOT RECOMMENDED
    # Time Complexity: O(2^(m+n)) - exponential
    # Space Complexity: O(m+n) - recursion stack
    # ========================================================================
    def uniquePathsWithObstacles_recursion(self, obstacleGrid: List[List[int]]) -> int:
        """
        Pure recursive solution - explores all possible paths.
        Very inefficient due to repeated subproblems.
        """
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        def dfs(i: int, j: int) -> int:
            # Out of bounds or hit an obstacle
            if i >= m or j >= n or obstacleGrid[i][j] == 1:
                return 0
            
            # Reached destination
            if i == m - 1 and j == n - 1:
                return 1
            
            # Count paths: down + right
            return dfs(i + 1, j) + dfs(i, j + 1)
        
        return dfs(0, 0)
    
    # ========================================================================
    # APPROACH 2: Recursion with Memoization (Top-Down DP)
    # Time Complexity: O(m*n) - each cell computed once
    # Space Complexity: O(m*n) - memo table + O(m+n) recursion stack
    # ========================================================================
    def uniquePathsWithObstacles_memoization(self, obstacleGrid: List[List[int]]) -> int:
        """
        Top-down DP with memoization.
        Caches computed results to avoid redundant calculations.
        """
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        memo = {}
        
        def dfs(i: int, j: int) -> int:
            # Out of bounds or hit an obstacle
            if i >= m or j >= n or obstacleGrid[i][j] == 1:
                return 0
            
            # Reached destination
            if i == m - 1 and j == n - 1:
                return 1
            
            # Return cached result if exists
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Calculate and cache result
            memo[(i, j)] = dfs(i + 1, j) + dfs(i, j + 1)
            return memo[(i, j)]
        
        return dfs(0, 0)
    
    # ========================================================================
    # APPROACH 3: Dynamic Programming (Bottom-Up) - 2D Array (CORRECTED VERSION)
    # Time Complexity: O(m*n) - iterate through all cells once
    # Space Complexity: O(m*n) - 2D DP table
    # ========================================================================
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        dp = [[1 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = 0
                elif i == 0 and j == 0:
                    dp[0][0] = dp[0][0]
                elif i == 0 and dp[0][j - 1] == 0:
                    dp[0][j] = 0
                elif j == 0 and dp[i - 1][0] == 0:
                    dp[i][0] = 0
                elif i != 0 and j != 0:
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        print(dp)
        return dp[m - 1][n - 1]

    
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        if obstacleGrid[0][0] == 1:
            return 0

        m, n = len(obstacleGrid), len(obstacleGrid[0])
        dp = [[0 for _ in range(n)] for _ in range(m)]
        dp[0][0] = 1

        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1 or (i == 0 and j == 0):
                    continue
                if i > 0:
                    dp[i][j] += dp[i - 1][j]
                if j > 0:
                    dp[i][j] += dp[i][j - 1]
        return dp[m - 1][n - 1]

    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        """
        Bottom-up DP solution - CORRECTED VERSION of your code.
        
        Key fixes:
        1. Initialize dp with 0s, not 1s
        2. Handle starting point obstacle
        3. Properly handle first row and column obstacles
        """
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        # If start or end has obstacle, no paths possible
        if obstacleGrid[0][0] == 1 or obstacleGrid[m-1][n-1] == 1:
            return 0
        
        # Initialize with 0s instead of 1s
        dp = [[0 for _ in range(n)] for _ in range(m)]
        
        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    # Obstacle: 0 paths through this cell
                    dp[i][j] = 0
                elif i == 0 and j == 0:
                    # Starting point
                    dp[0][0] = 1
                elif i == 0:
                    # First row: can only come from left
                    # If previous cell is blocked (0 paths), this is also 0
                    dp[0][j] = dp[0][j - 1]
                elif j == 0:
                    # First column: can only come from above
                    dp[i][0] = dp[i - 1][0]
                else:
                    # Regular cell: sum of paths from above and left
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        
        return dp[m - 1][n - 1]
    
    # ========================================================================
    # APPROACH 4: Space-Optimized DP - 1D Array
    # Time Complexity: O(m*n)
    # Space Complexity: O(n) - only one row needed
    # ========================================================================
    def uniquePathsWithObstacles_optimized_1d(self, obstacleGrid: List[List[int]]) -> int:
        """
        Space-optimized version using 1D array.
        Reduces space from O(m*n) to O(n).
        """
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        # Early exit if start or end blocked
        if obstacleGrid[0][0] == 1 or obstacleGrid[m-1][n-1] == 1:
            return 0
        
        dp = [0] * n
        
        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    dp[j] = 0  # Obstacle blocks all paths
                elif i == 0 and j == 0:
                    dp[0] = 1  # Starting point
                elif i == 0:
                    dp[j] = dp[j - 1]  # First row
                elif j == 0:
                    # dp[0] already has value from previous row (above)
                    dp[0] = dp[0]
                else:
                    # dp[j] = from above (previous iteration, not updated yet)
                    # dp[j-1] = from left (current iteration, just updated)
                    dp[j] = dp[j] + dp[j - 1]
        
        return dp[n - 1]
    
    # ========================================================================
    # APPROACH 5: In-Place Modification (Most Space Efficient)
    # Time Complexity: O(m*n)
    # Space Complexity: O(1) - modifies input
    # NOTE: Modifies the input grid - not always acceptable!
    # ========================================================================
    def uniquePathsWithObstacles_inplace(self, obstacleGrid: List[List[int]]) -> int:
        """
        Most space-efficient: modifies input grid directly.
        
        Strategy: Use the grid itself to store path counts.
        - 0 (empty) becomes the number of paths to reach that cell
        - 1 (obstacle) stays 1, then becomes 0
        """
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        # Early exit
        if obstacleGrid[0][0] == 1 or obstacleGrid[m-1][n-1] == 1:
            return 0
        
        # Set starting point
        obstacleGrid[0][0] = 1
        
        # Initialize first row
        for j in range(1, n):
            if obstacleGrid[0][j] == 1:
                obstacleGrid[0][j] = 0
            else:
                obstacleGrid[0][j] = obstacleGrid[0][j - 1]
        
        # Initialize first column
        for i in range(1, m):
            if obstacleGrid[i][0] == 1:
                obstacleGrid[i][0] = 0
            else:
                obstacleGrid[i][0] = obstacleGrid[i - 1][0]
        
        # Fill rest of grid
        for i in range(1, m):
            for j in range(1, n):
                if obstacleGrid[i][j] == 1:
                    obstacleGrid[i][j] = 0
                else:
                    obstacleGrid[i][j] = obstacleGrid[i - 1][j] + obstacleGrid[i][j - 1]
        
        return obstacleGrid[m - 1][n - 1]


# ============================================================================
# ISSUES IN YOUR ORIGINAL CODE (Fixed Above)
# ============================================================================
"""
Problems with your original implementation:

1. ❌ Initialized dp with 1s instead of 0s
   dp = [[1 for _ in range(n)] for _ in range(m)]
   This causes incorrect counts for cells that should be unreachable.

2. ❌ Incomplete handling of first row/column obstacles
   elif i == 0 and dp[0][j - 1] == 0:
       dp[0][j] = 0
   This doesn't propagate the block correctly. Should be: dp[0][j] = dp[0][j-1]

3. ❌ Redundant condition
   elif i == 0 and j == 0:
       dp[0][0] = dp[0][0]
   This does nothing since dp[0][0] is already 1.

4. ⚠️  Missing early exit check
   Should check if start/end position has obstacle before processing.
"""


# ============================================================================
# EXAMPLES & TEST CASES
# ============================================================================
"""
Example 1:
Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
Output: 2

Visualization:
[0, 0, 0]     [1, 1, 1]
[0, 1, 0]  -> [1, 0, 1]
[0, 0, 0]     [1, 1, 2]

Paths:
1. Right -> Right -> Down -> Down
2. Down -> Down -> Right -> Right

Example 2:
Input: obstacleGrid = [[0,1],[0,0]]
Output: 1

Visualization:
[0, 1]     [1, 0]
[0, 0]  -> [1, 1]

Only 1 path: Down -> Right (can't go right first due to obstacle)

Example 3 (Edge case):
Input: obstacleGrid = [[1]]
Output: 0
(Starting position itself is an obstacle)
"""


# ============================================================================
# COMPARISON SUMMARY
# ============================================================================
"""
┌──────────────────────┬─────────────────┬─────────────────┬──────────────────┐
│ Approach             │ Time Complexity │ Space Complexity│ Notes            │
├──────────────────────┼─────────────────┼─────────────────┼──────────────────┤
│ 1. Pure Recursion    │ O(2^(m+n))      │ O(m+n)          │ Too slow         │
│ 2. Memoization       │ O(m*n)          │ O(m*n) + stack  │ Good for learning│
│ 3. 2D DP             │ O(m*n)          │ O(m*n)          │ ✅ Recommended   │
│ 4. 1D DP Array       │ O(m*n)          │ O(n)            │ Space optimized  │
│ 5. In-place          │ O(m*n)          │ O(1)            │ Modifies input   │
└──────────────────────┴─────────────────┴─────────────────┴──────────────────┘

RECOMMENDATION:
- For interviews: Approach 3 (2D DP) - clear logic, easy to explain
- For tight memory: Approach 4 (1D array)
- Only if allowed: Approach 5 (in-place)

KEY INSIGHT:
- If cell has obstacle: paths = 0
- If cell is reachable: paths = paths_from_above + paths_from_left
- First row/column need special handling (can only come from one direction)
- Always check if start/end positions have obstacles!
"""