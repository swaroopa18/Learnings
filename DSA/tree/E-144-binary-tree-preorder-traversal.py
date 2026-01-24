# Definition for a binary tree node.
from typing import Optional, List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ========================================
# APPROACH 1: Iterative Preorder Traversal
# ========================================
# Time Complexity: O(n) - visit each node once
# Space Complexity: O(h) - stack depth equals tree height
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # Handle empty tree
        if not root:
            return []
        
        stack, res = [root], []
        
        while stack:
            # Pop from stack and process immediately (Root first)
            curr = stack.pop()
            res.append(curr.val)
            
            # Push right child first (so left is processed first - LIFO)
            # Stack is LIFO, so we push right before left
            if curr.right:
                stack.append(curr.right)
            if curr.left:
                stack.append(curr.left)
        
        return res


# ========================================
# APPROACH 2: Recursive Preorder Traversal
# ========================================
# Time Complexity: O(n) - visit each node once
# Space Complexity: O(h) - recursion call stack depth
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def pre(node, res):
            if node is None:
                return
            
            # Preorder traversal: Root -> Left -> Right
            res.append(node.val)       # Visit current node FIRST
            pre(node.left, res)        # Traverse left subtree
            pre(node.right, res)       # Traverse right subtree

        res = []
        pre(root, res)
        return res


# ========================================
# APPROACH 3: Morris Traversal (Advanced)
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(1) - No stack or recursion!
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        curr = root
        
        while curr:
            # If no left child, process current and move to right
            if not curr.left:
                res.append(curr.val)
                curr = curr.right
            else:
                # Find the inorder predecessor (rightmost node in left subtree)
                predecessor = curr.left
                while predecessor.right and predecessor.right != curr:
                    predecessor = predecessor.right
                
                # Create temporary link
                if not predecessor.right:
                    res.append(curr.val)  # Process node BEFORE going left (preorder)
                    predecessor.right = curr
                    curr = curr.left
                else:
                    # Remove temporary link and move to right subtree
                    predecessor.right = None
                    curr = curr.right
        
        return res

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
# Preorder traversal result: [1, 2, 4, 5, 3]
# Order: Root -> Left -> Right
#
# Step-by-step for iterative approach:
# 1. Stack: [1]          -> Process 1, push [3, 2]
# 2. Stack: [3, 2]       -> Process 2, push [3, 5, 4]
# 3. Stack: [3, 5, 4]    -> Process 4
# 4. Stack: [3, 5]       -> Process 5
# 5. Stack: [3]          -> Process 3
# Result: [1, 2, 4, 5, 3]


# ========================================
# KEY DIFFERENCES: Preorder vs Inorder
# ========================================
# PREORDER:  Root -> Left -> Right (process node BEFORE children)
# INORDER:   Left -> Root -> Right (process node BETWEEN children)
# POSTORDER: Left -> Right -> Root (process node AFTER children)
#
# Use Cases:
# - Preorder: Copy/serialize tree, prefix expression evaluation
# - Inorder: Get sorted values from BST
# - Postorder: Delete tree, postfix expression evaluation