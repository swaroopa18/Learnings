# https://leetcode.com/problems/fibonacci-number/
# F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1

# ============================================================================
# APPROACH 1: SPACE-OPTIMIZED ITERATIVE (BEST)
# ============================================================================
class Solution1:
    def fib(self, n: int) -> int:
        """
        Time Complexity: O(n) - single loop from 2 to n
        Space Complexity: O(1) - only using two variables
        """
        if n <= 1:
            return n
            
        prev1, prev2 = 0, 1  # F(0), F(1)

        for _ in range(2, n + 1):
            curr_sum = prev1 + prev2  # F(i) = F(i-1) + F(i-2)
            prev1 = prev2             # Update F(i-2) for next iteration
            prev2 = curr_sum          # Update F(i-1) for next iteration

        return prev2  # prev2 now holds F(n)


# ============================================================================
# APPROACH 2: TOP-DOWN DYNAMIC PROGRAMMING (MEMOIZATION)
# ============================================================================
class Solution2:
    def fib(self, n: int) -> int:
        """
        Time Complexity: O(n) - each subproblem computed once
        Space Complexity: O(n) - memoization table + recursion stack
        """
        memo = {}
        
        def helper(x):
            if x <= 1:
                return x
            if x in memo:
                return memo[x]
            
            memo[x] = helper(x - 1) + helper(x - 2)
            return memo[x]
        
        return helper(n)


# ============================================================================
# APPROACH 3: BOTTOM-UP DYNAMIC PROGRAMMING (TABULATION)
# ============================================================================
class Solution3:
    def fib(self, n: int) -> int:
        """        
        Time Complexity: O(n) - single loop to fill array
        Space Complexity: O(n) - DP array of size n+1
        """
        if n <= 1:
            return n
            
        dp = [0] * (n + 1)
        dp[0], dp[1] = 0, 1  # Base cases

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]

"""
DETAILED ANALYSIS:
**COMPLEXITY PROGRESSION**:
   - Naive recursion: O(2^n) time, O(n) space - NEVER use
   - Memoized recursion: O(n) time, O(n) space - Good
   - Tabulation: O(n) time, O(n) space - Good
   - Space-optimized: O(n) time, O(1) space - BEST
   - Matrix exponentiation: O(log n) time, O(1) space - Advanced
"""