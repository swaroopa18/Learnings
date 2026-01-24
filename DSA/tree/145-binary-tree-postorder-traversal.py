# Definition for a binary tree node.
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ========================================
# APPROACH 1: Recursive Postorder Traversal
# ========================================
# Time Complexity: O(n) - visit each node once
# Space Complexity: O(h) - recursion call stack depth
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def post(node, res):
            # Base case: if node is None, return
            if node is None:
                return
            
            # Postorder traversal: Left -> Right -> Root
            post(node.left, res)       # Traverse left subtree
            post(node.right, res)      # Traverse right subtree
            res.append(node.val)       # Visit current node LAST

        res = []
        post(root, res)
        return res


# ========================================
# APPROACH 2: Two-Stack Iterative (Easiest to understand)
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(n) - uses two stacks
# Logic: Reverse of preorder (Root->Right->Left becomes Left->Right->Root)
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        
        stack1, stack2 = [root], []
        
        # Stack1: Do modified preorder (Root -> Right -> Left)
        while stack1:
            node = stack1.pop()
            stack2.append(node)  # Push to second stack
            
            # Push left first, then right (opposite of preorder)
            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)
        
        # Stack2 now has nodes in reverse postorder
        # Pop from stack2 to get postorder
        res = []
        while stack2:
            res.append(stack2.pop().val)
        
        return res


# ========================================
# APPROACH 3: One-Stack Iterative (Most Efficient)
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(h) - single stack
# Logic: Track last visited node to avoid revisiting right subtree
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = []
        result = []
        lastVisited = None  # Track last processed node
        curr = root

        while curr or stack:
            # Go to leftmost node
            if curr:
                stack.append(curr)
                curr = curr.left
            else:
                # Peek at top of stack
                node = stack[-1]
                
                # If right child exists and hasn't been visited, go right
                if node.right and lastVisited != node.right:
                    curr = node.right
                else:
                    # Process node (both children done or no right child)
                    result.append(node.val)
                    lastVisited = stack.pop()

        return result


# ========================================
# APPROACH 4: Two-Stack with Reverse (Alternative)
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(n)
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        
        stack = [root]
        res = []
        
        # Modified preorder: Root -> Right -> Left
        while stack:
            node = stack.pop()
            res.append(node.val)
            
            # Push left first, then right
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        
        # Reverse to get Left -> Right -> Root
        return res[::-1]


# ========================================
# APPROACH 5: Morris Traversal (Advanced - O(1) Space)
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(1) - no stack or recursion!
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        curr = root
        
        while curr:
            # If no right child, process and go left
            if not curr.right:
                res.append(curr.val)
                curr = curr.left
            else:
                # Find predecessor (leftmost in right subtree)
                predecessor = curr.right
                while predecessor.left and predecessor.left != curr:
                    predecessor = predecessor.left
                
                if not predecessor.left:
                    # Create thread
                    res.append(curr.val)
                    predecessor.left = curr
                    curr = curr.right
                else:
                    # Remove thread
                    predecessor.left = None
                    curr = curr.left
        
        # Reverse result for postorder
        return res[::-1]


# ========================================
# EXAMPLE USAGE & VISUALIZATION
# ========================================
# Tree structure:
#       1
#      / \
#     2   3
#    / \
#   4   5
#
# Postorder traversal result: [4, 5, 2, 3, 1]
# Order: Left -> Right -> Root (process node LAST)
#
# Step-by-step execution (One-Stack approach):
# 1. Go left: 1 -> 2 -> 4
# 2. Process 4 (no children)
# 3. Back to 2, go right to 5
# 4. Process 5 (no children)
# 5. Process 2 (both children done)
# 6. Back to 1, go right to 3
# 7. Process 3 (no children)
# 8. Process 1 (both children done)
# Result: [4, 5, 2, 3, 1]


# ========================================
# COMPARISON OF APPROACHES
# ========================================
"""
| Approach           | Time | Space | Difficulty | Notes                        |
|--------------------|------|-------|------------|------------------------------|
| Recursive          | O(n) | O(h)  | Easy       | Simplest, intuitive          |
| Two-Stack          | O(n) | O(n)  | Easy       | Easy to understand logic     |
| One-Stack          | O(n) | O(h)  | Medium     | Most efficient iterative     |
| Reverse Preorder   | O(n) | O(n)  | Easy       | Simple trick, uses reverse   |
| Morris             | O(n) | O(1)  | Hard       | Best space, complex logic    |
"""


# ========================================
# KEY INSIGHTS
# ========================================
"""
1. POSTORDER PATTERN: Left -> Right -> Root (children before parent)

2. WHY POSTORDER IS TRICKY:
   - Must ensure both children are processed before parent
   - Need to track if right subtree has been visited
   - Can't process node immediately when popped from stack

3. TWO-STACK TRICK:
   - Do reverse preorder (Root -> Right -> Left)
   - Reverse result to get (Left -> Right -> Root)
   - Easier than one-stack but uses more space

4. ONE-STACK APPROACH:
   - Use lastVisited to avoid re-processing right subtree
   - Peek at stack top instead of popping immediately
   - More efficient but requires careful logic

5. USE CASES:
   - Deleting/freeing tree nodes (delete children first)
   - Postfix expression evaluation
   - Bottom-up tree processing
   - Dependency resolution (process dependencies first)
"""


# ========================================
# COMMON MISTAKES TO AVOID
# ========================================
"""
❌ Processing node immediately when popped (that's preorder!)
❌ Not tracking last visited node in one-stack approach
❌ Forgetting to check if right child has been visited
❌ Incorrect order: pushing right before left in two-stack

✅ Remember: Children must be processed BEFORE parent
✅ Use lastVisited to track completion of right subtree
✅ Two-stack is easier to understand and implement
✅ One-stack is more space-efficient for interviews
"""