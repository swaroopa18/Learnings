# https://leetcode.com/problems/backspace-string-compare/description/

# SOLUTION 1: Reverse Iteration with String Building
# SC: O(n), TC: O(n)
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def removeBackSpace(st):
            backspaces = 0
            cleanstr = ""
            # Iterate from right to left to handle backspaces correctly
            for i in range(len(st) - 1, -1, -1):
                if st[i] == "#":
                    # Count backspaces we need to apply
                    backspaces += 1
                elif st[i] != "#" and backspaces > 0:
                    # Skip this character because we have pending backspaces
                    backspaces -= 1
                else:
                    # Valid character - add to result string
                    # Note: we're building backwards, so final string will be reversed
                    cleanstr += st[i]
            return cleanstr
        
        # Compare the processed strings (both will be reversed but consistently so)
        return removeBackSpace(s) == removeBackSpace(t)


# SOLUTION 2: Stack-based Approach (Most Intuitive)
# SC: O(n), TC: O(n)
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def removeBackSpace(st):
            stack = []
            # Process characters left to right
            for char in st:
                if char == "#":
                    # Backspace: remove last character if stack not empty
                    if len(stack) > 0:
                        stack.pop()
                else:
                    # Regular character: add to stack
                    stack.append(char)
            return stack

        # Compare the final stacks (representing the processed strings)
        return removeBackSpace(s) == removeBackSpace(t)


# SOLUTION 3: Two-Pointer Approach (Space Optimized)
# SC: O(1), TC: O(n) - Most efficient solution
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def getNextValidIdx(st, idx):
            """
            Find the next valid character index, handling backspaces
            Returns the index of the next character that wouldn't be deleted
            """
            skip = 0
            # Iterate backwards from given index
            for i in range(idx, -1, -1):
                if st[i] == "#":
                    # Found backspace - increment skip counter
                    skip += 1
                elif st[i] != "#" and skip > 0:
                    # Found character but we need to skip it due to backspace
                    skip -= 1
                else:
                    # Found valid character that won't be deleted
                    return i
            # No valid character found
            return -1

        # Start from the end of both strings
        i, j = len(s) - 1, len(t) - 1
        
        # Continue until we've processed both strings completely
        while i >= 0 or j >= 0:
            # Get next valid character indices for both strings
            i = getNextValidIdx(s, i)
            j = getNextValidIdx(t, j)
            
            # Both strings have valid characters to compare
            if i >= 0 and j >= 0:
                if s[i] != t[j]:
                    return False
            # One string has characters left, the other doesn't
            elif i >= 0 or j >= 0:
                return False
            
            # Move to next characters
            i -= 1
            j -= 1
        
        # Successfully compared all characters
        return True


"""
COMPARISON OF APPROACHES:

1. Reverse Iteration (Solution 1):
   - Builds strings by processing right-to-left
   - Simple logic but creates reversed strings
   - Time: O(n), Space: O(n)

2. Stack Approach (Solution 2):
   - Most intuitive - mimics typing with backspace
   - Uses stack data structure naturally
   - Time: O(n), Space: O(n)

3. Two-Pointer Approach (Solution 3):
   - Most space-efficient - no extra data structures
   - More complex logic but optimal space usage
   - Time: O(n), Space: O(1)

Example walkthrough with s="ab#c", t="ad#c":
- Stack approach: s → ['a','c'], t → ['a','c'] → True
- Two-pointer: compares 'c'=='c' ✓, then 'a'=='a' ✓ → True
"""