# Definition for a binary tree node.
from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ========================================
# APPROACH 1: Recursive DFS (Most Elegant)
# ========================================
# Time Complexity: O(n) - visit each node once
# Space Complexity: O(h) - recursion stack depth (O(log n) balanced, O(n) skewed)
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        
        # Recursively find max depth of left and right subtrees
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        
        # Current depth = 1 + max of subtree depths
        return 1 + max(left_depth, right_depth)


# ========================================
# APPROACH 2: BFS Level Order Traversal
# ========================================
# Time Complexity: O(n) - visit each node once
# Space Complexity: O(w) - queue width, worst case O(n) for complete tree
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        
        queue = deque([root])
        level = 0
        
        while queue:
            level += 1  # Increment depth for each level
            size = len(queue)  # Number of nodes at current level
            
            # Process all nodes at current level
            for _ in range(size):
                node = queue.popleft()
                
                # Add children to queue for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return level


# ========================================
# APPROACH 3: Iterative DFS with Stack
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(h) - stack depth
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        # Stack stores (node, current_depth) tuples
        stack = [(root, 1)]
        max_depth = 0
        
        while stack:
            node, depth = stack.pop()
            max_depth = max(max_depth, depth)
            
            # Push children with incremented depth
            if node.right:
                stack.append((node.right, depth + 1))
            if node.left:
                stack.append((node.left, depth + 1))
        
        return max_depth


# ========================================
# APPROACH 4: Recursive DFS (One-liner)
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(h)
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        return 0 if not root else 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


# ========================================
# APPROACH 5: BFS with Tuple (Alternative)
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(w)
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        queue = deque([(root, 1)])  # (node, depth)
        max_depth = 0
        
        while queue:
            node, depth = queue.popleft()
            max_depth = max(max_depth, depth)
            
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))
        
        return max_depth


# ========================================
# EXAMPLE USAGE & VISUALIZATION
# ========================================
"""
Tree structure:
        3
       / \
      9  20
        /  \
       15   7

Max Depth: 3

Level-by-level breakdown:
Level 1: [3]           -> depth = 1
Level 2: [9, 20]       -> depth = 2
Level 3: [15, 7]       -> depth = 3

Recursive DFS trace for node 3:
- maxDepth(3) = 1 + max(maxDepth(9), maxDepth(20))
- maxDepth(9) = 1 + max(0, 0) = 1
- maxDepth(20) = 1 + max(maxDepth(15), maxDepth(7))
  - maxDepth(15) = 1 + max(0, 0) = 1
  - maxDepth(7) = 1 + max(0, 0) = 1
  - maxDepth(20) = 1 + max(1, 1) = 2
- maxDepth(3) = 1 + max(1, 2) = 3
"""


# ========================================
# COMPARISON OF APPROACHES
# ========================================
"""
| Approach        | Time | Space      | Pros                           | Cons                    |
|-----------------|------|------------|--------------------------------|-------------------------|
| Recursive DFS   | O(n) | O(h)       | Clean, intuitive, minimal code | Stack overflow risk     |
| BFS Level Order | O(n) | O(w)       | Iterative, clear level logic   | More code, uses queue   |
| Iterative DFS   | O(n) | O(h)       | No recursion, explicit control | More verbose            |
| One-liner       | O(n) | O(h)       | Very concise                   | Less readable           |

Where:
- n = number of nodes
- h = height of tree (best: log n, worst: n)
- w = maximum width (worst: n/2 for complete tree)
"""


# ========================================
# KEY INSIGHTS
# ========================================
"""
1. DEPTH vs HEIGHT:
   - Depth: distance from root to node
   - Height: distance from node to deepest leaf
   - Max depth = Height of tree

2. DFS vs BFS FOR DEPTH:
   - DFS (Recursive): More elegant, less space for balanced trees
   - BFS: Better for very deep trees (avoid stack overflow)
   - BFS: Natural fit for level-based problems

3. SPACE COMPLEXITY:
   - Balanced tree: DFS uses O(log n), BFS uses O(n/2) ≈ O(n)
   - Skewed tree: Both use O(n)
   - DFS generally more space-efficient

4. WHEN TO USE EACH:
   - Recursive DFS: Default choice, interviews, clean code
   - BFS: Need level information, very deep trees
   - Iterative DFS: Avoid recursion limits, similar to recursive
"""


# ========================================
# RELATED PROBLEMS
# ========================================
"""
1. Minimum Depth of Binary Tree (LeetCode 111)
   - Use BFS (stop at first leaf)
   - Or DFS with careful null handling

2. Balanced Binary Tree (LeetCode 110)
   - Check if |left_depth - right_depth| <= 1 for all nodes

3. Diameter of Binary Tree (LeetCode 543)
   - Similar recursion, but max(left + right) instead of max(left, right)

4. Maximum Depth of N-ary Tree (LeetCode 559)
   - Same logic, iterate through all children
"""


# ========================================
# COMMON MISTAKES TO AVOID
# ========================================
"""
❌ Forgetting base case (null check)
❌ Not using len(queue) before the loop in BFS
❌ Incrementing level inside the for loop
❌ Confusing depth with number of nodes

✅ Always handle null/empty tree case
✅ Process entire level before incrementing depth
✅ Remember: depth is counted by edges or nodes (typically nodes)
✅ Test with single node (depth = 1) and empty tree (depth = 0)
"""


# ========================================
# INTERVIEW TIPS
# ========================================
"""
1. Start with recursive solution (easiest to explain)
2. If asked for iterative, use BFS (more intuitive than iterative DFS)
3. Discuss space complexity trade-offs
4. Mention that for very deep trees, BFS avoids stack overflow
5. Can optimize by stopping BFS early if only checking if depth > k
"""


# ========================================
# EDGE CASES TO CONSIDER
# ========================================
"""
1. Empty tree (root = None) -> return 0
2. Single node -> return 1
3. Left-skewed tree (like linked list) -> depth = n
4. Right-skewed tree -> depth = n
5. Balanced tree -> depth = log(n) + 1
6. Complete binary tree -> depth = floor(log2(n)) + 1
"""