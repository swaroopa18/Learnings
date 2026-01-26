# Definition for a binary tree node.
from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """
        Check if a binary tree is symmetric around its center.
        
        APPROACH 1: ITERATIVE BFS (Current Implementation)
        - Use a queue to compare nodes in mirror positions
        - Time: O(n), Space: O(n) where n is number of nodes
        - Good for wide trees, avoids stack overflow
        """
        if root is None:
            return True
        
        queue = deque([(root.left, root.right)])
        
        while queue:
            node1, node2 = queue.popleft()
            
            # Both nodes are None - symmetric at this position
            if node1 is None and node2 is None:
                continue
            
            # One node is None, other isn't - not symmetric
            if node1 is None or node2 is None:
                return False
            
            # Values don't match - not symmetric
            if node1.val != node2.val:
                return False
            
            # Add children in mirror order:
            # Compare left child of node1 with right child of node2
            queue.append((node1.left, node2.right))
            # Compare right child of node1 with left child of node2
            queue.append((node1.right, node2.left))
        
        return True


"""
APPROACH 2: RECURSIVE DFS
- Cleaner code, more intuitive
- Time: O(n), Space: O(h) where h is height (call stack)
- Better for balanced trees
"""
def isSymmetric(root: Optional[TreeNode]) -> bool:
    def isMirror(t1, t2):
        # Both empty - symmetric
        if not t1 and not t2:
            return True
        # One empty - not symmetric
        if not t1 or not t2:
            return False
        # Check: same value AND left mirrors right AND right mirrors left
        return (t1.val == t2.val and 
                isMirror(t1.left, t2.right) and 
                isMirror(t1.right, t2.left))
    
    return isMirror(root.left, root.right) if root else True

"""
APPROACH 3: ITERATIVE WITH STACK (DFS)
- Similar to BFS but uses stack instead of queue
- Time: O(n), Space: O(n)
- DFS traversal order instead of level-order
"""
def isSymmetric(root: Optional[TreeNode]) -> bool:
    if not root:
        return True
    
    stack = [(root.left, root.right)]
    
    while stack:
        node1, node2 = stack.pop()
        
        if not node1 and not node2:
            continue
        if not node1 or not node2:
            return False
        if node1.val != node2.val:
            return False
        
        # Push in specific order for DFS
        stack.append((node1.left, node2.right))
        stack.append((node1.right, node2.left))
    
    return True

"""
COMPLEXITY COMPARISON:
┌──────────┬─────────────┬─────────────┬────────────────┐
│ Approach │ Time        │ Space       │ Best For       │
├──────────┼─────────────┼─────────────┼────────────────┤
│ BFS      │ O(n)        │ O(w)        │ Wide trees     │
│ DFS Rec  │ O(n)        │ O(h)        │ Balanced trees │
│ DFS Iter │ O(n)        │ O(h)        │ Deep trees     │
└──────────┴─────────────┴─────────────┴────────────────┘
where w = max width, h = height

EXAMPLE:
    1
   / \
  2   2
 / \ / \
3  4 4  3
-> Symmetric ✓

    1
   / \
  2   2
   \   \
   3    3
-> Not symmetric ✗ (different structure)
"""