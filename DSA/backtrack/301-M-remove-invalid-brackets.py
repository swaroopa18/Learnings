# Remove Invalid Parentheses - LeetCode Problem Analysis
# https://leetcode.com/problems/remove-invalid-parentheses/description/

from collections import deque
from typing import List

# ==================================================================================
# APPROACH 1: BRUTE FORCE DFS (WORST APPROACH)
# Time: O(2^n) - tries all possible combinations
# Space: O(n) - recursion depth + expression building
# ==================================================================================

def removeInvalidParentheses_bruteforce(s):
    """
    WORST APPROACH: Pure brute force trying all combinations
    
    Problems:
    - Generates ALL possible subsequences (2^n)
    - No pruning or early termination
    - Inefficient validity checking
    - High memory usage due to set operations
    """
    result = set()
    min_removed = [float('inf')]  # Using list to make it mutable inside recursion

    def is_valid(expr):
        count = 0
        for char in expr:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    return False
        return count == 0

    def dfs(index, expr, removed_count):
        # Base case: finished processing
        if index == len(s):
            expr_str = "".join(expr)
            if is_valid(expr_str):
                if removed_count < min_removed[0]:
                    min_removed[0] = removed_count
                    result.clear()
                    result.add(expr_str)
                elif removed_count == min_removed[0]:
                    result.add(expr_str)
            return

        char = s[index]

        # OPTION 1: Remove current character if it's a parenthesis
        if char in '()':
            dfs(index + 1, expr, removed_count + 1)

        # OPTION 2: Keep current character
        expr.append(char)
        dfs(index + 1, expr, removed_count)
        expr.pop()  # Backtrack

    dfs(0, [], 0)
    return list(result)


# ==================================================================================
# APPROACH 2: OPTIMIZED DFS WITH PRUNING (BETTER APPROACH)
# Time: O(2^n) worst case, but with significant pruning
# Space: O(n) - recursion depth + visited set can grow large
# ==================================================================================

class Solution_DFS:
    def getInvalidCount(self, s):
        """Calculate minimum removals needed"""
        stack = []
        for char in s:
            if char == "(":
                stack.append(char)
            elif char == ")":
                if stack and stack[-1] == "(":
                    stack.pop()
                else:
                    stack.append(char)
        return len(stack)

    def removeInvalidParentheses(self, s: str) -> List[str]:
        """
        BETTER APPROACH: DFS with pruning
        
        Improvements over brute force:
        - Pre-calculates minimum removals needed
        - Uses visited set to avoid duplicate work
        - Prunes invalid branches early
        
        Issues:
        - Still explores many unnecessary paths
        - visited set can become very large
        - Not guaranteed to find shortest path first
        """
        min_removal = self.getInvalidCount(s)
        result = set()
        visited = set()

        def backtrack(removals_left, curr):
            if curr in visited:
                return
            visited.add(curr)

            if removals_left < 0:
                return

            if self.getInvalidCount(curr) == 0:
                result.add(curr)
                return

            for i in range(len(curr)):
                if curr[i] not in ('(', ')'):
                    continue
                next_str = curr[:i] + curr[i+1:]
                backtrack(removals_left - 1, next_str)

        backtrack(min_removal, s)
        return list(result) if len(result) > 0 else [""]


# ==================================================================================
# APPROACH 3: BFS LEVEL-ORDER TRAVERSAL (BEST APPROACH)
# Time: O(n * 2^n) worst case, but finds optimal solution at first valid level
# Space: O(2^n) for queue and visited set
# ==================================================================================

class Solution_BFS:
    def isValid(self, s):
        """Check if parentheses are balanced"""
        count = 0
        for ch in s:
            if ch == "(":
                count += 1
            elif ch == ")":
                count -= 1
                if count < 0:
                    return False
        return count == 0

    def removeInvalidParentheses(self, s: str) -> List[str]:
        """
        BEST APPROACH: BFS Level-order traversal
        
        Advantages:
        - Guarantees minimum removals (finds shortest path first)
        - Stops as soon as valid solutions are found
        - Level-by-level exploration ensures optimality
        - Natural pruning - once valid level found, no need to go deeper
        
        Why it's optimal:
        - BFS explores by removal count (0 removals, then 1, then 2, etc.)
        - First valid strings found are guaranteed to have minimum removals
        - Visited set prevents exploring duplicate states
        """
        result = set()
        visited = set()

        queue = deque([s])
        found = False

        while queue:
            curr = queue.popleft()
            
            if self.isValid(curr):
                result.add(curr)
                found = True
            
            # If we found valid solutions at this level, don't explore further
            if found:
                continue

            # Generate all possible strings by removing one parenthesis
            for i in range(len(curr)):
                if curr[i] not in "()":
                    continue
                next_str = curr[:i] + curr[i + 1:]
                if next_str not in visited:
                    visited.add(next_str)
                    queue.append(next_str)
        
        return list(result)


# ==================================================================================
# APPROACH 4: OPTIMIZED BFS WITH EARLY TERMINATION (BEST OPTIMIZED)
# Time: O(n * 2^n) worst case, but significantly faster in practice
# Space: O(2^n) for queue and visited set
# ==================================================================================

class Solution_Optimized:
    def isValid(self, s):
        """Optimized validity check with early termination"""
        count = 0
        for ch in s:
            if ch == "(":
                count += 1
            elif ch == ")":
                count -= 1
                if count < 0:  # Early termination
                    return False
        return count == 0

    def removeInvalidParentheses(self, s: str) -> List[str]:
        """
        OPTIMIZED APPROACH: BFS with improvements
        
        Optimizations:
        - Early termination in validity check
        - Process entire level before checking next level
        - More efficient string operations
        - Better memory management
        """
        if not s:
            return [""]
        
        result = []
        visited = {s}
        queue = deque([s])
        
        while queue:
            level_size = len(queue)
            level_found = False
            
            # Process entire current level
            for _ in range(level_size):
                curr = queue.popleft()
                
                if self.isValid(curr):
                    result.append(curr)
                    level_found = True
            
            # If we found valid solutions at this level, return immediately
            if level_found:
                return result
            
            # Generate next level
            for _ in range(level_size):
                if queue:  # Safety check
                    curr = queue.popleft()
                    for i in range(len(curr)):
                        if curr[i] in "()":
                            next_str = curr[:i] + curr[i + 1:]
                            if next_str not in visited:
                                visited.add(next_str)
                                queue.append(next_str)
        
        return [""]


# ==================================================================================
# COMPLEXITY ANALYSIS SUMMARY
# ==================================================================================

"""
RANKING (WORST TO BEST):

1. BRUTE FORCE DFS:
   - Time: O(2^n) - explores all subsequences
   - Space: O(n) - recursion stack
   - No pruning, very inefficient

2. OPTIMIZED DFS:
   - Time: O(2^n) - still exponential but with pruning
   - Space: O(n + 2^n) - recursion + visited set
   - Better than brute force but still not optimal

3. BFS APPROACH:
   - Time: O(n * 2^n) - worst case, but finds optimal solution first
   - Space: O(2^n) - queue and visited set
   - Guarantees minimum removals

4. OPTIMIZED BFS:
   - Time: O(n * 2^n) - same worst case but faster in practice
   - Space: O(2^n) - optimized memory usage
   - Best practical performance

KEY INSIGHTS:
- BFS is superior because it finds the minimum removal solution first
- DFS might explore many unnecessary deep paths
- The problem is inherently exponential, but BFS provides better guarantees
- Early termination and pruning are crucial for performance
"""

# Example usage:
if __name__ == "__main__":
    solution = Solution_Optimized()
    test_cases = [
        "()())",
        "(((",
        "()",
        "((a))",
        ")(",
    ]
    
    for test in test_cases:
        result = solution.removeInvalidParentheses(test)
        print(f"Input: '{test}' -> Output: {result}")