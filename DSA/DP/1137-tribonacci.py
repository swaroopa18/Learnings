# https://leetcode.com/problems/n-th-tribonacci-number/description/

# T(0) = 0, T(1) = 1, T(2) = 1, T(n) = T(n-1) + T(n-2) + T(n-3) for n > 2

# ============================================================================
# APPROACH 1: TOP-DOWN DYNAMIC PROGRAMMING (MEMOIZATION)
# ============================================================================
class Solution:
    def tribonacci(self, n: int) -> int:
        """
        Time Complexity: O(n) - each value computed once and cached
        Space Complexity: O(n) - memoization dictionary + recursion stack depth
        """
        mem = {0: 0, 1: 1, 2: 1}

        def helper(x):
            if x in mem:
                return mem[x]
            mem[x] = helper(x - 1) + helper(x - 2) + helper(x - 3)
            return mem[x]

        return helper(n)


# ============================================================================
# APPROACH 2: SPACE-OPTIMIZED ITERATIVE (BEST)
# ============================================================================
class Solution1:
    def tribonacci2(self, n: int) -> int:
        """
        Time Complexity: O(n) - single loop from 3 to n
        Space Complexity: O(1) - only using three variables
        """
        t0, t1, t2 = 0, 1, 1
        if n == 0:
            return t0
        if n == 1:
            return t1
        if n == 2:
            return t2
            
        for _ in range(3, n + 1):
            curr_sum = t2 + t1 + t0
            t0 = t1
            t1 = t2
            t2 = curr_sum

        return t2


# ============================================================================
# BONUS: TABULATION APPROACH
# ============================================================================
class SolutionTabulation:
    def tribonacci(self, n: int) -> int:
        """
        Time Complexity: O(n) - single loop to fill array
        Space Complexity: O(n) - DP array of size n+1
        """
        if n <= 2:
            return 1 if n >= 1 else 0
            
        dp = [0] * (n + 1)
        dp[0], dp[1], dp[2] = 0, 1, 1
        
        for i in range(3, n + 1):
            dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
            
        return dp[n]

