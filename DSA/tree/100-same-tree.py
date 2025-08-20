# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque
from typing import Optional

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Time Complexity: O(min(m, n)) where m and n are the number of nodes in trees p and q
        Space Complexity: O(min(m, n)) for the queues storing nodes at each level
        """
        q1, q2 = deque([p]), deque([q])
        
        while q1 and q2:
            node1, node2 = q1.popleft(), q2.popleft()
            val1 = node1.val if node1 else None
            val2 = node2.val if node2 else None

            if val1 != val2:
                return False
                
            # Only add children if both nodes exist (not None)
            if node1:
                q1.append(node1.left)
                q1.append(node1.right)
            if node2:
                q2.append(node2.left)
                q2.append(node2.right)
                
        # Trees are same if both queues are empty (same structure)
        return not q1 and not q2


# Alternative Approach 1: Recursive DFS (More intuitive and cleaner)
class SolutionDFS:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """        
        Time Complexity: O(min(m, n))
        Space Complexity: O(min(h1, h2)) where h1, h2 are heights of the trees
        """
        # Base cases
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
            
        return (self.isSameTree(p.left, q.left) and 
                self.isSameTree(p.right, q.right))


# Alternative Approach 2: Iterative DFS with Stack
class SolutionIterativeDFS:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Iterative DFS using stack - good for avoiding recursion stack overflow.
        
        Time Complexity: O(min(m, n))
        Space Complexity: O(min(h1, h2)) for the stack
        """
        stack = [(p, q)]
        
        while stack:
            node1, node2 = stack.pop()
            
            if not node1 and not node2:
                continue
            if not node1 or not node2:
                return False
            if node1.val != node2.val:
                return False
                
            stack.append((node1.left, node2.left))
            stack.append((node1.right, node2.right))
            
        return True


# Alternative Approach 3: Serialize and Compare (Less efficient but interesting)
class SolutionSerialize:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Serialize both trees and compare strings.
        
        Time Complexity: O(m + n)
        Space Complexity: O(m + n) for storing serialized strings
        
        Note: Less efficient as it always visits all nodes, but can be useful
        for certain scenarios like caching serialized representations.
        """
        def serialize(node):
            if not node:
                return "null"
            return f"{node.val},{serialize(node.left)},{serialize(node.right)}"
        
        return serialize(p) == serialize(q)


"""
NOTES:

1. **Best Approach**: Recursive DFS (SolutionDFS) is generally preferred because:
   - Clean and intuitive code
   - Natural tree traversal pattern
   - Early termination on differences
   - Good space complexity O(h) instead of O(w) where w can be large

2. **Original BFS Approach**: Works correctly but has some considerations:
   - Uses more space O(w) where w is maximum width of tree
   - Still efficient with early termination
   - Good for level-by-level comparison if needed

3. **When to use each**:
   - Recursive DFS: Default choice for most cases
   - Iterative DFS: When recursion depth might be an issue
   - BFS: When you need level-order comparison
   - Serialize: When you need to cache/store tree representations

4. **Optimization notes**:
   - All approaches have early termination
   - Recursive is most readable and typically fastest
   - Space complexity varies: O(h) for DFS, O(w) for BFS
   - For balanced trees: h = O(log n), w = O(n/2)
   - For skewed trees: h = O(n), w = O(1)

5. **Edge cases handled**:
   - Both trees null: True
   - One tree null: False  
   - Different values: False
   - Different structures: False
"""