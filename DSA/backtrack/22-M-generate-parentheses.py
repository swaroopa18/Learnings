# https://leetcode.com/problems/generate-parentheses/

from typing import List


# APPROACH 1: BRUTE FORCE WITH INSERTION
# Time Complexity: O(4^n / √n) - Catalan number with overhead from duplicates
# Space Complexity: O(4^n / √n) - storing all combinations including duplicates
class Solution1:
    def generateParenthesis(self, n: int) -> List[str]:
        """
        BRUTE FORCE APPROACH:
        - Start with base case "()" 
        - For each iteration, insert "()" at every possible position
        - Use set to remove duplicates at the end
        
        PROBLEMS WITH THIS APPROACH:
        1. Generates many duplicate combinations
        2. Inefficient due to string concatenation in loops
        3. Extra space needed for duplicate removal
        4. No pruning of invalid states
        """
        output = ['()']  # Base case for n=1
        
        # Build combinations for n=2 to n
        for _ in range(1, n):
            new_set = []
            for pattern in output:
                # Try inserting "()" at every position (0 to middle+1)
                for i in range((len(pattern) // 2) + 1):
                    new_patt = pattern[:i] + "()" + pattern[i:]
                    new_set.append(new_patt)
            output = new_set[:]
        
        # Remove duplicates using set conversion
        return list(set(output))


# APPROACH 2: BACKTRACKING (OPTIMAL)
# Time Complexity: O(4^n / √n) - Catalan number, but no duplicate generation
# Space Complexity: O(n) - recursion stack depth + current string length
class Solution2:
    def generateParenthesis(self, n: int) -> List[str]:
        """
        BACKTRACKING APPROACH (RECOMMENDED):
        - Build valid combinations character by character
        - Use constraints to avoid invalid states:
          * Add '(' only if we haven't used all n opening brackets
          * Add ')' only if it won't exceed opening brackets count
        - No duplicates generated, so no need for deduplication
        
        ADVANTAGES:
        1. Generates only valid combinations
        2. No duplicate generation
        3. Efficient pruning using constraints
        4. Optimal time complexity for this problem
        """
        result = []

        def backtrack(op, cl, curr):
            """
            Args:
                op: count of opening brackets used so far
                cl: count of closing brackets used so far  
                curr: current string being built
            """
            # Base case: used all n opening and n closing brackets
            if op == cl == n:
                result.append("".join(curr))
                return
            
            # Add opening bracket if we haven't used all n
            if op < n:
                curr.append("(")
                backtrack(op + 1, cl, curr)
                curr.pop()  # Backtrack
            
            # Add closing bracket if it won't exceed opening brackets
            if cl < op:
                curr.append(")")
                backtrack(op, cl + 1, curr)
                curr.pop()  # Backtrack

        backtrack(0, 0, [])
        return result


# APPROACH 3: DYNAMIC PROGRAMMING (ALTERNATIVE)
# Time Complexity: O(4^n / √n) - Catalan number
# Space Complexity: O(4^n / √n) - storing all valid combinations
class Solution3:
    def generateParenthesis(self, n: int) -> List[str]:
        """
        DYNAMIC PROGRAMMING APPROACH:
        - Build solutions bottom-up using previously computed results
        - For each i, generate combinations using the recurrence:
          f(i) = "(" + f(p) + ")" + f(q) where p + q = i - 1
        
        CHARACTERISTICS:
        1. Avoids recursion overhead
        2. Reuses previously computed results
        3. Still generates Catalan number of combinations
        4. Good for multiple queries with different n values
        """
        if n == 0:
            return [""]
        
        # dp[i] stores all valid combinations for i pairs
        dp = [[] for _ in range(n + 1)]
        dp[0] = [""]
        
        for i in range(1, n + 1):
            for p in range(i):
                q = i - 1 - p
                # Combine f(p) and f(q) with outer parentheses
                for left in dp[p]:
                    for right in dp[q]:
                        dp[i].append(f"({left}){right}")
        
        return dp[n]


"""
COMPLEXITY ANALYSIS:

The number of valid parentheses combinations is the n-th Catalan number:
C(n) = (1/(n+1)) * (2n choose n) = O(4^n / √n)

All three approaches have the same theoretical time complexity, but differ in:

1. **Approach 1 (Brute Force)**: 
   - Generates duplicates, requires deduplication
   - String concatenation overhead
   - Less efficient in practice

2. **Approach 2 (Backtracking)**: 
   - Most efficient in practice
   - No duplicate generation
   - Minimal space overhead
   - **RECOMMENDED SOLUTION**

3. **Approach 3 (Dynamic Programming)**:
   - Good for multiple queries
   - No recursion overhead
   - Higher space complexity due to memoization

MATHEMATICAL INSIGHT:
The problem is equivalent to finding the number of ways to arrange n pairs of 
parentheses such that they are properly nested. This is precisely the definition 
of the n-th Catalan number.
"""