# CLIMBING STAIRS - LEETCODE PROBLEM ANALYSIS

# APPROACH 1: NAIVE RECURSION
# 👉 Problem idea:
# If you are at step n, you can reach there from:

# step n-1 (taking 1 step)
# step n-2 (taking 2 steps)
# So brute force = try all possibilities using recursion.
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        return self.climbStairs(n - 1) + self.climbStairs(n - 2)

# TIME COMPLEXITY: O(2^n) - exponential, very slow, because each call makes two recursive calls (n-1 and n-2),
# causing the same subproblems to be recomputed multiple times.
# Each function call branches into 2 more calls (n-1 and n-2), so the recursion forms a binary tree.
# A binary tree with height n has about 2ⁿ nodes, so the total number of calls is O(2ⁿ).

# SPACE COMPLEXITY: O(n) - recursion stack depth
# PROBLEM: Recalculates same subproblems multiple times
# Example: climbStairs(5) calls climbStairs(3) twice independently


# APPROACH 2: MEMOIZATION (TOP-DOWN DP)
class Solution:
    memory = {1: 1, 2: 2}  # WARNING: Class variable shared across instances!

    def climbStairs(self, n: int) -> int:
        if n in self.memory:
            return self.memory[n]
        self.memory[n] = self.climbStairs(n - 1) + self.climbStairs(n - 2)
        return self.memory[n]

# TIME COMPLEXITY: O(n) - each subproblem computed once
# SPACE COMPLEXITY: O(n) - memoization dict + recursion stack
# ISSUE: Class variable causes problems with multiple test cases


# APPROACH 3: BETTER MEMOIZATION (FIXED)
class Solution:
    def climbStairs(self, n: int) -> int:
        memo = {}
        
        def dp(n):
            if n == 1:
                return 1
            if n == 2:
                return 2
            if n in memo:
                return memo[n]
            memo[n] = dp(n - 1) + dp(n - 2)
            return memo[n]
        
        return dp(n)

# TIME COMPLEXITY: O(n)
# SPACE COMPLEXITY: O(n) - memo dict + recursion stack
# ADVANTAGE: Clean, no shared state issues


# APPROACH 4: BOTTOM-UP DP (TABULATION)
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]

# TIME COMPLEXITY: O(n) - single loop
# SPACE COMPLEXITY: O(n) - dp array
# ADVANTAGE: No recursion, iterative approach


# APPROACH 5: SPACE-OPTIMIZED DP (BEST)
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        prev2 = 1  # f(n-2)
        prev1 = 2  # f(n-1)
        
        for i in range(3, n + 1):
            current = prev1 + prev2
            prev2 = prev1
            prev1 = current
        
        return prev1
    
class Solution:
    def climbStairs(self, n: int) -> int:
            prev1, prev2 = 1, 1
            for _ in range(0, n - 1):
                temp = prev2
                prev2 = prev1 + prev2
                prev1 = temp
            return prev2

# TIME COMPLEXITY: O(n) - single loop
# SPACE COMPLEXITY: O(1) - only using 3 variables
# ADVANTAGE: Optimal space usage, fastest in practice


# APPROACH 6: MATHEMATICAL FORMULA (ADVANCED)
import math

class Solution:
    def climbStairs(self, n: int) -> int:
        # Binet's formula for Fibonacci numbers
        sqrt5 = math.sqrt(5)
        phi = (1 + sqrt5) / 2  # Golden ratio
        psi = (1 - sqrt5) / 2
        
        # F(n+1) where F is Fibonacci sequence
        return round((phi**(n+1) - psi**(n+1)) / sqrt5)

# TIME COMPLEXITY: O(1) - constant time
# SPACE COMPLEXITY: O(1) - constant space
# NOTE: May have floating point precision issues for very large n


# PERFORMANCE COMPARISON:
# n=10:   Naive: ~100 calls, Optimized: 10 operations
# n=20:   Naive: ~21,000 calls, Optimized: 20 operations  
# n=40:   Naive: ~2.6 billion calls, Optimized: 40 operations

# RECOMMENDED SOLUTION: Space-optimized DP (Approach 5)
# - Easy to understand and implement
# - Optimal time and space complexity
# - No precision issues like mathematical formula