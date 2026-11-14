"""
LeetCode 110 - Balanced Binary Tree
-------------------------------------
A binary tree is height-balanced if, for EVERY node, the heights of its left
and right subtrees differ by at most 1. Return True if the tree is balanced.

Example:
        3
       / \
      9  20
         / \
        15  7
    heights at 20: left 1, right 1 -> ok; at 3: left 1, right 2 -> ok
    answer: True

        1
       / \
      2   2
     / \
    3   3
   / \
  4   4
    at node 2 (left child of root): left height 3, right height 1 -> diff 2
    answer: False

The key point: the condition must hold at EVERY node, not just the root. A
tree can have a balanced root and still be unbalanced deep inside.

Two approaches are given below.

Summary
-------
 #  Approach                              Time        Space   Notes
 1  Top-down (BFS + height recompute)     O(n * h)    O(n)    Your first version, recomputes heights repeatedly
 2  Bottom-up (height with -1 flag)       O(n)        O(h)    RECOMMENDED, each node visited once

 (h = height of the tree: O(log n) if balanced, O(n) if skewed)
"""

from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class SolutionTopDown:
    """
    Approach 1: Top-Down (BFS over nodes, recompute height at each)
    -----------------------------------------------------------------
    Idea:
      - Write a plain helper dfs(node) that returns the height of a subtree.
      - Visit every node of the tree with a BFS queue. At each node, compute
        the height of its left and right subtrees and check that they differ
        by at most 1. If any node fails, return False.
      - If every node passes, return True.

    Walkthrough on 1 -> (2 -> (3 -> (4, 4), 3), 2):
        root 1: left height 3, right height 1 -> diff 2 > 1 -> False

    Why it is slower:
      - dfs() walks the WHOLE subtree every time it is called. A node deep in
        the tree gets walked again for each of its ancestors' checks. The
        same heights are computed over and over.
      - Each node is walked once per ancestor, so the total work is about
        n * (depth of the tree).

    Time Complexity:  O(n * h) -- O(n log n) for a balanced tree, and it can
                      grow towards O(n^2) for a lopsided one. The early
                      return on the first failure helps in many cases, but
                      do not count on it.
    Space Complexity: O(n) -- the BFS queue can hold a full level of nodes
                      (plus O(h) recursion for dfs).

    Things to be aware of:
      - It is correct. The problem is only the repeated work.
      - Having the height function and the balance check as two separate
        jobs is what causes the waste. Approach 2 merges them.
    """

    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True

        def dfs(node):
            if node is None:
                return 0
            left = dfs(node.left)
            right = dfs(node.right)
            return 1 + max(left, right)

        queue = deque([root])

        while queue:
            node = queue.popleft()
            if abs(dfs(node.left) - dfs(node.right)) > 1:
                return False
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return True


class Solution:
    """
    Approach 2 (RECOMMENDED): Bottom-Up DFS with a -1 "unbalanced" Flag
    ---------------------------------------------------------------------
    Idea:
      - Let dfs(node) return the height of the subtree IF it is balanced,
        and the special value -1 if it is NOT balanced anywhere inside.
      - Post-order: get the heights of the left and right subtrees first.
          * If either child already returned -1, pass -1 straight up.
          * If their heights differ by more than 1, this node breaks the
            rule, so return -1.
          * Otherwise return 1 + max(left, right) as the normal height.
      - The tree is balanced exactly when dfs(root) is not -1.

    Walkthrough on 3 -> (9, 20 -> (15, 7)):
        dfs(9)  = 1,  dfs(15) = 1,  dfs(7) = 1
        dfs(20): |1 - 1| = 0 -> height 2
        dfs(3):  |1 - 2| = 1 -> height 3
        3 != -1 -> True

    Walkthrough on the unbalanced example:
        dfs(4) = 1 (both), dfs(3) = 2, other dfs(3) = 1
        dfs(2, left side): |2 - 1| = 1 -> height 3
        dfs(2, right side) = 1
        dfs(1): |3 - 1| = 2 > 1 -> -1 -> False

    Why it is faster:
      - Each node is visited exactly once, and its height is computed once
        and reused by its parent. Height and balance are checked in the same
        pass, so nothing is recomputed.
      - Once a -1 appears it travels up through every ancestor without any
        more height work.

    Time Complexity:  O(n) -- every node is visited once.
    Space Complexity: O(h) -- recursion depth equals the tree height
                      (O(log n) balanced, O(n) in the worst skewed case).

    Things to be aware of:
      - Using -1 is safe because a real height is never negative (an empty
        tree is 0), so -1 cannot be confused with a valid height.
      - Heights are only meaningful when the subtree is balanced. Once a
        subtree is unbalanced we no longer care about its height, which is
        why returning -1 in its place loses nothing.

    Common pitfalls:
      - Forgetting the `left == -1 or right == -1` check. Without it, an
        unbalanced subtree deep down would be hidden if the levels above it
        happen to look balanced.
      - Checking only the root's two heights instead of every node.
    """

    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True

        def dfs(node):
            if node is None:
                return 0
            left = dfs(node.left)
            right = dfs(node.right)
            if left == -1 or right == -1:
                return -1
            if abs(left - right) > 1:
                return -1
            return 1 + max(left, right)

        return dfs(root) != -1