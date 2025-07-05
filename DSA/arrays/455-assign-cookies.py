# https://leetcode.com/problems/assign-cookies/description/

from typing import List

# =============================================================================
# APPROACH: Greedy Algorithm with Two Pointers - OPTIMAL SOLUTION
# =============================================================================
# TC: O(n log n + m log m) where n = len(g), m = len(s)
# SC: O(1)

class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        """
        Greedy approach: Match least greedy child with smallest suitable cookie.
        
        Key Insight: If we can't satisfy a less greedy child with a cookie,
        we definitely can't satisfy a more greedy child with the same cookie.
        
        Strategy:
        1. Sort both arrays
        2. Use two pointers to match children with cookies
        3. Always try to satisfy the least greedy child first
        4. Use the smallest possible cookie for each child
        """
        
        # Sort both arrays to enable greedy matching
        g.sort()  # Sort children by greed factor (ascending): [1, 2, 3, 4]
        s.sort()  # Sort cookies by size (ascending): [1, 1, 2, 3]
        
        # Two pointers for traversal
        child = cookie = content = 0
        
        while child < len(g) and cookie < len(s):
            if s[cookie] >= g[child]:
                content += 1
                child += 1
            cookie += 1
        
        return content
# =============================================================================
# WHY GREEDY WORKS
# =============================================================================
"""
Greedy Choice Property:
- If we can satisfy child i with cookie j, and child i+1 with cookie j+1,
  then we can also satisfy child i with cookie j+1 (since cookie_j+1 >= cookie_j)
- But we should prefer using cookie j for child i to save cookie j+1 for more greedy children
- This proves that the greedy choice (smallest suitable cookie) is always optimal

Optimal Substructure:
- After making a greedy choice, the remaining problem has the same structure
- We can solve it optimally using the same greedy strategy
"""