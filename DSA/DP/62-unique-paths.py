from typing import List
import math


class Solution:
    """
    Problem: Unique Paths
    
    There is a robot on an m x n grid. The robot is initially located at the 
    top-left corner (i.e., grid[0][0]). The robot tries to move to the 
    bottom-right corner (i.e., grid[m-1][n-1]). The robot can only move 
    either down or right at any point in time.
    
    Given the two integers m and n, return the number of possible unique paths 
    that the robot can take to reach the bottom-right corner.
    """
    
    # ========================================================================
    # APPROACH 1: Pure Recursion (Brute Force) - NOT RECOMMENDED
    # Time Complexity: O(2^(m+n)) - exponential, explores all paths
    # Space Complexity: O(m+n) - recursion stack depth
    # ========================================================================
    def uniquePaths_recursion(self, m: int, n: int) -> int:
        """
        Pure recursive solution - explores all possible paths.
        Extremely inefficient due to massive repeated subproblems.

        If you're at position (i, j):
        Total paths to (i, j) = paths to (i-1, j) + paths to (i, j-1)
        If you're at the destination (bottom-right), there's exactly 1 way (you're already there!)
        If you go out of bounds, there are 0 ways
        """
        def dfs(row, col):
            if row == m - 1 and col == n - 1:
                return 1
            # Out od bounds
            if row >= m or col >= n:
                return 0
            return dfs(row + 1, col) + dfs(row, col + 1)

        return dfs(0, 0)
    
    # ========================================================================
    # APPROACH 2: Recursion with Memoization (Top-Down DP)
    # Time Complexity: O(m*n) - each cell computed once
    # Space Complexity: O(m*n) - memo table + O(m+n) recursion stack
    # ========================================================================
    def uniquePaths_memoization(self, m: int, n: int) -> int:
        """
        Top-down DP with memoization.
        Caches results to avoid recomputing the same subproblems.
        """
        memo = [[-1 for _ in range(n)] for _ in range(m)]

        def dfs(row, col):
            if row == m - 1 and col == n - 1:
                return 1
            if row >= m or col >= n:
                return 0
            if memo[row][col] != -1:
                return memo[row][col]
                
            memo[row][col] = dfs(row + 1, col) + dfs(row, col + 1)
            return memo[row][col]

        return dfs(0, 0)
    
    # ========================================================================
    # APPROACH 3: Dynamic Programming (Bottom-Up) - 2D Array
    # Time Complexity: O(m*n) - iterate through all cells
    # Space Complexity: O(m*n) - 2D DP table
    # ========================================================================
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Bottom-up DP solution (YOUR ORIGINAL APPROACH - CORRECT!).
        
        Key insight:
        - First row and first column all have 1 path (can only go one direction)
        - For any other cell: paths = paths_from_above + paths_from_left
        
        This is already optimal for a 2D DP approach!
        """
        # Initialize entire grid with 1s
        # First row: can only go right (1 path each)
        # First column: can only go down (1 path each)
        dp = [[1] * n for _ in range(m)]
        
        # Fill the rest of the grid
        for i in range(1, m):
            for j in range(1, n):
                # Current cell paths = paths from above + paths from left
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        
        return dp[m - 1][n - 1]
    
    # ========================================================================
    # APPROACH 4: Space-Optimized DP - 1D Array (Rolling Array)
    # Time Complexity: O(m*n) - still process all cells
    # Space Complexity: O(n) - only one row needed
    # ========================================================================
    def uniquePaths_optimized_1d(self, m: int, n: int) -> int:
        """
        Space-optimized version using 1D array.
        
        Key insight: We only need the previous row and current row values.
        Since we process left-to-right, we can reuse the same array.
        
        - dp[j] initially holds the value from the row above (previous iteration)
        - dp[j-1] holds the value from the left (current iteration)
        """
        # Initialize with all 1s (represents first row)
        dp = [1] * n
        
        # Process each row
        for i in range(1, m):
            for j in range(1, n):
                # dp[j] currently has value from above (previous row)
                # dp[j-1] has value from left (current row, just updated)
                dp[j] = dp[j] + dp[j - 1]
        
        return dp[n - 1]
    
    # ========================================================================
    # APPROACH 5: Even More Space-Optimized - Single Row with Rolling Update
    # Time Complexity: O(m*n)
    # Space Complexity: O(min(m,n)) - use smaller dimension
    # ========================================================================
    def uniquePaths_optimized_min_space(self, m: int, n: int) -> int:
        """
        Further optimization: always use the smaller dimension for our array.
        If m > n, we can transpose our thinking and use n-sized array.
        """
        # Use smaller dimension for space efficiency
        if m > n:
            m, n = n, m
        
        dp = [1] * m
        
        for j in range(1, n):
            for i in range(1, m):
                dp[i] = dp[i] + dp[i - 1]
        
        return dp[m - 1]
    
    # ========================================================================
    # APPROACH 6: Mathematical Solution (Combinatorics) - MOST EFFICIENT!
    # Time Complexity: O(m+n) or O(min(m,n)) - for computing combinations
    # Space Complexity: O(1) - only variables
    # ========================================================================
    def uniquePaths_math(self, m: int, n: int) -> int:
        """
        Mathematical solution using combinatorics - BEST APPROACH!
        
        Insight: To reach (m-1, n-1) from (0,0):
        - We need exactly (m-1) down moves and (n-1) right moves
        - Total moves = (m-1) + (n-1) = m+n-2
        - Problem becomes: "Choose (m-1) positions for down moves from (m+n-2) total"
        
        Answer = C(m+n-2, m-1) = (m+n-2)! / ((m-1)! * (n-1)!)
        
        This is the OPTIMAL solution in terms of both time and space!
        """
        # Total steps needed
        total_steps = m + n - 2
        # Down steps (or right steps, doesn't matter)
        down_steps = m - 1
        
        # Calculate C(total_steps, down_steps) efficiently
        # C(n, k) = n! / (k! * (n-k)!)
        # Optimized: C(n, k) = (n * (n-1) * ... * (n-k+1)) / (k * (k-1) * ... * 1)
        
        return math.comb(total_steps, down_steps)
    
    # Alternative implementation without using math.comb
    def uniquePaths_math_manual(self, m: int, n: int) -> int:
        """
        Manual calculation of combinations without using math library.
        Avoids overflow by dividing as we multiply.
        """
        total_steps = m + n - 2
        down_steps = min(m - 1, n - 1)  # Use smaller for efficiency
        
        result = 1
        for i in range(down_steps):
            # Multiply by (total_steps - i) and divide by (i + 1)
            result = result * (total_steps - i) // (i + 1)
        
        return result


# ============================================================================
# VISUAL EXAMPLES
# ============================================================================
"""
Example 1: m = 3, n = 7
Grid visualization (showing number of paths to reach each cell):

    0   1   2   3   4   5   6
  ┌───┬───┬───┬───┬───┬───┬───┐
0 │ 1 │ 1 │ 1 │ 1 │ 1 │ 1 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┤
1 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │
  ├───┼───┼───┼───┼───┼───┼───┤
2 │ 1 │ 3 │ 6 │10 │15 │21 │28 │
  └───┴───┴───┴───┴───┴───┴───┘

Answer: 28 unique paths

Example 2: m = 3, n = 2
Grid visualization:

    0   1
  ┌───┬───┐
0 │ 1 │ 1 │
  ├───┼───┤
1 │ 1 │ 2 │
  ├───┼───┤
2 │ 1 │ 3 │
  └───┴───┘

Answer: 3 unique paths
Paths: 
1. Right -> Down -> Down
2. Down -> Right -> Down
3. Down -> Down -> Right

Mathematical verification for Example 1:
- Total moves needed: (3-1) + (7-1) = 2 + 6 = 8 moves
- Down moves needed: 2
- C(8, 2) = 8! / (2! * 6!) = (8 * 7) / (2 * 1) = 56 / 2 = 28 ✓
"""


# ============================================================================
# COMPARISON SUMMARY
# ============================================================================
"""
┌──────────────────────┬─────────────────┬─────────────────┬──────────────────────┐
│ Approach             │ Time Complexity │ Space Complexity│ Notes                │
├──────────────────────┼─────────────────┼─────────────────┼──────────────────────┤
│ 1. Pure Recursion    │ O(2^(m+n))      │ O(m+n)          │ ❌ Too slow          │
│ 2. Memoization       │ O(m*n)          │ O(m*n) + stack  │ Good for learning    │
│ 3. 2D DP (Original)  │ O(m*n)          │ O(m*n)          │ ✅ Clear & standard  │
│ 4. 1D DP Array       │ O(m*n)          │ O(n)            │ Space optimized      │
│ 5. Min Dimension     │ O(m*n)          │ O(min(m,n))     │ Better space opt     │
│ 6. Math (Combinat.)  │ O(m+n)          │ O(1)            │ ⭐ BEST - Optimal!  │
└──────────────────────┴─────────────────┴─────────────────┴──────────────────────┘

RECOMMENDATION BY CONTEXT:

🎯 For Interviews (Coding Question):
   - Start with Approach 3 (2D DP) - your original solution is perfect!
   - Mention you can optimize to O(n) space with Approach 4
   - If interviewer asks for best solution, present Approach 6 (Math)

🚀 For Production/Best Performance:
   - Use Approach 6 (Mathematical) - it's O(m+n) time and O(1) space!
   - Most elegant and efficient

📚 For Learning DP:
   - Study Approaches 2 and 3 to understand DP patterns
   - Practice both top-down (memoization) and bottom-up (tabulation)

YOUR ORIGINAL CODE ANALYSIS:
✅ Correct logic
✅ Clean implementation  
✅ Optimal for 2D DP approach
✅ Good variable naming
✅ No bugs!

Minor note: Your code is already excellent! The only "upgrade" would be:
- Space optimization (Approach 4): O(n) instead of O(m*n)
- Mathematical approach (Approach 6): O(m+n) time, O(1) space
"""


# ============================================================================
# WHY THE MATHEMATICAL APPROACH WORKS
# ============================================================================
"""
🎯 INTUITION: This is a PERMUTATION problem!

Think of it this way:
- From (0,0) to (m-1, n-1), you make exactly (m+n-2) moves
- Of these moves, exactly (m-1) must be DOWN and (n-1) must be RIGHT
- The question is: "In how many ways can we arrange these moves?"

Example: m=3, n=3 (need 2 downs, 2 rights = 4 total moves)
- Moves can be represented as: D D R R
- Different arrangements: DDRR, DRDR, DRRD, RDDR, RDRD, RRDD
- This is choosing 2 positions for D from 4 total positions
- C(4,2) = 6 ✓

Formula: C(m+n-2, m-1) or equivalently C(m+n-2, n-1)

This transforms a DP problem into a pure math problem!
"""