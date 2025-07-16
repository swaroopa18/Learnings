# https://leetcode.com/problems/letter-combinations-of-a-phone-number/

"""
Problem: Given a string containing digits from 2-9 inclusive, return all possible letter 
combinations that the number could represent. Return the answer in any order.

Example: Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
"""

from typing import List
from itertools import product


# =============================================================================
# INITIAL PREP - Understanding the problem step by step
# =============================================================================

def letters(digits='abc'):
    """Single letter printing - Understanding basic iteration"""
    result = []
    
    def backtrack(index):
        if index >= len(digits):
            return
        result.append(digits[index])
        backtrack(index + 1)
        
    backtrack(0)
    print(result)  # ['a', 'b', 'c']


def two_combinations(a1, a2):
    """2-combinations - Understanding cross product of two groups"""
    result = []
    
    def backtrack(i):
        if i >= len(a1):
            return
        for j in range(len(a2)):
            result.append(a1[i] + a2[j])
        backtrack(i + 1)
        
    backtrack(0)
    print(result)

# Example usage
# two_combinations('abc', 'def')  # ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']


# =============================================================================
# APPROACH 1: BACKTRACKING (Your Original Solution - Enhanced)
# =============================================================================

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """
        Backtracking approach to generate all letter combinations.
        
        Time Complexity: O(3^N × 4^M) where N is number of digits mapping to 3 letters,
                        M is number of digits mapping to 4 letters
        Space Complexity: O(3^N × 4^M) for output + O(N) for recursion stack
        
        Args:
            digits: String of digits 2-9
            
        Returns:
            List of all possible letter combinations
        """
        if not digits:
            return []
            
        # Phone keypad mapping
        phone_map = {
            "2": "abc",
            "3": "def", 
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",  # 4 letters
            "8": "tuv",
            "9": "wxyz",  # 4 letters
        }
        
        # Convert digits to corresponding letter groups
        groups = [phone_map[digit] for digit in digits]
        result = []
        
        def backtrack(idx, path):
            # Base case: we've built a complete combination
            if idx == len(groups):
                result.append(path)
                return
            
            # Try each letter in the current group
            for char in groups[idx]:
                backtrack(idx + 1, path + char)
        
        backtrack(0, "")
        return result


# =============================================================================
# APPROACH 2: ITERATIVE WITH QUEUE (BFS-like)
# =============================================================================

class SolutionIterative:
    def letterCombinations(self, digits: str) -> List[str]:
        """
        Iterative approach using queue to build combinations level by level.
        
        Time Complexity: O(3^N × 4^M) - same as backtracking
        Space Complexity: O(3^N × 4^M) for output + O(3^N × 4^M) for queue
        
        More memory intensive but easier to understand for some.
        """
        if not digits:
            return []
            
        phone_map = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
        }
        
        # Start with empty string in queue
        queue = [""]
        
        for digit in digits:
            letters = phone_map[digit]
            next_queue = []
            
            # For each existing combination, append each possible letter
            for combination in queue:
                for letter in letters:
                    next_queue.append(combination + letter)
            
            queue = next_queue
        
        return queue

"""
COMPLEXITY ANALYSIS:
- Time Complexity: O(3^N × 4^M) where:
  * N = number of digits that map to 3 letters (2,3,4,5,6,8)
  * M = number of digits that map to 4 letters (7,9)
  * We need to generate all possible combinations
  
- Space Complexity: O(3^N × 4^M) for storing all combinations + recursion stack O(N)

APPROACH COMPARISON:

1. Backtracking (Original):
   ✅ Most intuitive for interviews
   ✅ Good for explaining thought process
   ✅ Easy to modify for additional constraints
   
2. Iterative/Queue:
   ✅ No recursion stack overhead
   ✅ Easy to understand flow
   ❌ Uses more memory for intermediate results
   
RECOMMENDATION:
- For interviews: Use Approach 1 (Backtracking) or 4 (Optimized Backtracking)
"""
