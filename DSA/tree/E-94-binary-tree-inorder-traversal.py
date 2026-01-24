# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
from typing import List, Optional

# ========================================
# APPROACH 1: Iterative Inorder Traversal
# ========================================
# Time Complexity: O(n) - visit each node once
# Space Complexity: O(h) - stack depth equals tree height
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack, res = [], []
        curr = root
        
        # Continue while there are nodes to process in stack or current node exists
        while stack or curr:
            # Traverse to the leftmost node, pushing all nodes onto stack
            while curr:
                stack.append(curr)
                curr = curr.left
            
            # Process the leftmost node (no more left children)
            curr = stack.pop()
            res.append(curr.val)  # Visit the node (inorder: left -> root -> right)
            
            # Move to right subtree
            curr = curr.right
            
        return res


# ========================================
# APPROACH 2: Recursive Inorder Traversal
# ========================================
# Time Complexity: O(n) - visit each node once
# Space Complexity: O(h) - recursion call stack depth equals tree height
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def inorder(node, res):
            # Base case: if node is None, return
            if node is None:
                return
            
            # Inorder traversal: Left -> Root -> Right
            inorder(node.left, res)      # Traverse left subtree
            res.append(node.val)          # Visit current node
            inorder(node.right, res)      # Traverse right subtree

        res = []
        inorder(root, res)
        return res


# ========================================
# EXAMPLE USAGE
# ========================================
# Tree structure:
#       1
#      / \
#     2   3
#    / \
#   4   5
#
# Inorder traversal result: [4, 2, 5, 1, 3]
# (visits nodes in sorted order for BST)