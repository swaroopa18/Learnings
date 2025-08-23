# ============================================================================
# PROBLEM: Unique Paths
# Find number of unique paths from top-left (0,0) to bottom-right (m-1,n-1)
# Can only move right or down
# ============================================================================

# ============================================================================
# SOLUTION 1: 2D DP (YOUR SOLUTION)
# ============================================================================
class Solution1:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Time Complexity: O(m*n) - visit each cell once
        Space Complexity: O(m*n) - 2D DP array
        
        Logic:
        - dp[i][j] = number of ways to reach cell (i,j)
        - Base case: first row and column all = 1 (only one way to reach)
        - Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]
        
        Clear and intuitive approach, good for understanding.
        """
        # Initialize DP table with 1s (base cases)
        dp = [[1] * n for _ in range(m)]
        
        # Fill the DP table
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        
        return dp[m - 1][n - 1]


# ============================================================================
# SOLUTION 2: SPACE-OPTIMIZED 1D DP (BEST)
# TC: O(m*n), SC: O(min(m,n))
# ============================================================================
class Solution2:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Space-optimized 1D DP using single array.
        
        Time Complexity: O(m*n) - same computation
        Space Complexity: O(min(m,n)) - only one row/column
        
        Key insight: we only need the previous row to compute current row.
        This is the OPTIMAL approach for interviews.
        """
        # Use smaller dimension for the array to minimize space
        if m < n:
            m, n = n, m
        
        # dp[j] represents number of ways to reach current row, column j
        dp = [1] * n
        
        for i in range(1, m):
            for j in range(1, n):
                # dp[j] = ways from above + ways from left
                dp[j] += dp[j - 1]
        
        return dp[n - 1]


# ============================================================================
# SOLUTION 3: MATHEMATICAL APPROACH (MOST EFFICIENT)
# TC: O(min(m,n)), SC: O(1)
# ============================================================================
class Solution3:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Mathematical approach using combinations.
        
        Time Complexity: O(min(m,n)) - computing combination
        Space Complexity: O(1) - no extra space
        
        Key insight: This is choosing (m-1) down moves from (m+n-2) total moves
        Formula: C(m+n-2, m-1) = (m+n-2)! / ((m-1)! * (n-1)!)
        """
        # We need (m-1) down moves and (n-1) right moves
        # Total moves = m + n - 2
        # Choose m-1 positions for down moves: C(m+n-2, m-1)
        
        total_moves = m + n - 2
        down_moves = m - 1
        
        # Compute C(total_moves, down_moves) efficiently
        # Use smaller of down_moves and right_moves to minimize computation
        k = min(down_moves, n - 1)
        
        result = 1
        for i in range(k):
            result = result * (total_moves - i) // (i + 1)
        
        return result


# ============================================================================
# SOLUTION 4: TOP-DOWN DP (MEMOIZATION)
# TC: O(m*n), SC: O(m*n)
# ============================================================================
class Solution4:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Time Complexity: O(m*n) - each cell computed once
        Space Complexity: O(m*n) - memoization + recursion stack
        
        Good for understanding recursive structure, but less efficient
        due to recursion overhead.
        """
        memo = {}
        
        def dfs(i, j):
            # Base cases
            if i == 0 or j == 0:
                return 1
            if i < 0 or j < 0:
                return 0
            
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Recurrence: ways from top + ways from left
            memo[(i, j)] = dfs(i - 1, j) + dfs(i, j - 1)
            return memo[(i, j)]
        
        return dfs(m - 1, n - 1)


"""
COMPREHENSIVE ANALYSIS:

1. **APPROACH RANKING** (by preference):
   a) Solution 2 (1D DP) - BEST for interviews ✅
   b) Solution 3 (Mathematical) - Most efficient but requires math knowledge
   c) Solution 1 (2D DP) - Good for learning/teaching
   d) Solution 4 (Top-down) - Educational but has overhead

2. **YOUR SOLUTION ANALYSIS**:
   - ✅ Correct and well-implemented
   - ✅ Clean initialization with base cases
   - ✅ Clear logic flow
   - ❌ Uses O(m*n) space when O(min(m,n)) is possible

3. **SPACE OPTIMIZATION** (Solution 1 → Solution 2):
   - Key insight: only need previous row to compute current row
   - Reduces space from O(m*n) to O(min(m,n))
   - Same time complexity, better space efficiency

4. **MATHEMATICAL SOLUTION INSIGHT**:
   - Problem = placing (m-1) down moves in (m+n-2) total moves
   - This is combination: C(m+n-2, m-1)
   - Most efficient but requires combinatorics knowledge

5. **COMPLEXITY COMPARISON**:
   ```
   Approach          Time         Space        Notes
   2D DP            O(m*n)       O(m*n)       Your solution
   1D DP            O(m*n)       O(min(m,n))  Optimal DP
   Mathematical     O(min(m,n))  O(1)         Most efficient
   Memoization      O(m*n)       O(m*n)       Recursion overhead
   ```

6. **INTERVIEW STRATEGY**:
   - Start with your 2D DP solution (shows understanding)
   - Optimize to 1D DP (demonstrates space optimization skills)  
   - Mention mathematical approach as bonus (shows mathematical thinking)
   - Discuss trade-offs between approaches

7. **WHEN TO USE EACH**:
   
   **2D DP**: 
   - Learning DP concepts
   - When clarity is more important than optimization
   - Building intuition for similar problems
   
   **1D DP**:
   - Production code (optimal balance)
   - Technical interviews
   - When space matters
   
   **Mathematical**:
   - When performance is critical
   - Competitive programming
   - When you're comfortable with combinatorics

8. **EDGE CASES**:
   - m = 1 or n = 1: return 1 (only one path)
   - m = n = 1: return 1
   - All solutions handle these correctly

9. **COMMON MISTAKES**:
   - Wrong base case initialization
   - Off-by-one errors in loop bounds
   - Not considering space optimization
   - Integer overflow in mathematical approach (for very large inputs)

10. **OPTIMIZATION NOTES**:
    - Your solution is correct and efficient
    - Main improvement: space optimization to O(min(m,n))
    - Mathematical solution exists but requires different thinking

RECOMMENDATION: Learn the progression from your 2D DP → 1D DP optimization.
This shows both understanding and optimization skills in interviews.
"""