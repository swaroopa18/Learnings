r"""
LeetCode 572 - Subtree of Another Tree
----------------------------------------
Given the roots of two binary trees root and subRoot, return True if there is
a subtree of root with the same structure and node values as subRoot. A
subtree of a tree is a node plus ALL of its descendants. The tree itself also
counts as a subtree of itself.

Example:
        3                4
       / \              / \
      4   5            1   2
     / \
    1   2
    root (left), subRoot (right) -> the left child of the root (4) with its
    descendants matches subRoot exactly -> True

        3                4
       / \              / \
      4   5            1   2
     / \
    1   2
       /
      0
    The node 4 now has an extra descendant 0 under 2, so no node of root
    matches subRoot exactly -> False

The key point: "same subtree" means the whole downward shape must match,
down to the leaves. Finding a node with the same value is not enough, and
finding a node whose first few levels match is not enough either. This is
why the check is "are these two trees identical" (LeetCode 100) applied at
every node of root.

Two approaches are given below. Both use the same helper isSameTree and
differ only in how they visit the nodes of root.

Summary
-------
 #  Approach                              Time        Space   Notes
 1  Recursion (try every node)            O(m * n)    O(h)    Short code, recursion depth can hit Python's limit
 2  BFS (try every node) (RECOMMENDED)    O(m * n)    O(m)    Same idea, no recursion on the main tree

 (m = nodes in root, n = nodes in subRoot, h = height of root)
"""

from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class SolutionRecursive:
    """
    Approach 1: Recursion (compare at every node)
    -----------------------------------------------
    Idea:
      - Write isSameTree(p, q): True when two trees are identical in both
        shape and values.
          * both empty              -> True
          * only one is empty       -> False
          * values differ           -> False
          * otherwise               -> left sides match AND right sides match
      - In isSubtree, first check whether root itself matches subRoot. If so,
        return True.
      - If root is empty there is nothing left to try, so return False.
      - Otherwise subRoot must be a subtree of the left side OR the right
        side, so recurse into both.

    Walkthrough on root = 3 -> (4 -> (1, 2), 5), subRoot = 4 -> (1, 2):
        isSameTree(3, 4): values differ -> False
        go left: isSameTree(4, 4): 4 == 4
                 left  isSameTree(1, 1) -> True
                 right isSameTree(2, 2) -> True
                 -> True, so the answer is True

    Why the order of the checks matters:
      - isSameTree(root, subRoot) is called before the `root is None`
        check. That is fine, because isSameTree handles None safely. If
        both were None it would return True, which is why an empty subRoot
        would match any empty spot. The problem guarantees subRoot is not
        empty, so this never gives a wrong answer here.

    Time Complexity:  O(m * n) -- in the worst case every node of root
                      starts a comparison that runs up to n steps. Many
                      comparisons stop after the first mismatch, so it is
                      usually much faster.
    Space Complexity: O(h) -- recursion depth (height of root), plus the
                      depth of the comparison, which is at most the height
                      of subRoot.

    Things to be aware of:
      - root can have up to 2000 nodes. A skewed tree of that size makes the
        recursion deeper than Python's default limit of 1000 and raises
        RecursionError. Approach 2 avoids recursion on root.

    Common pitfalls:
      - Comparing only the node values instead of the whole subtree.
      - Stopping at the first node whose value equals subRoot.val. A match
        in value may still differ further down, and a different node deeper
        in the tree may be the real match. Keep searching.
    """

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def isSameTree(p, q):
            if not p and not q:
                return True
            if not p or not q:
                return False
            if p.val != q.val:
                return False
            return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)

        if isSameTree(root, subRoot):
            return True
        if root is None:
            return False
        return self.isSubtree(root.left, subRoot) or self.isSubtree(
            root.right, subRoot
        )


class Solution:
    """
    Approach 2 (RECOMMENDED): BFS (compare at every node)
    -------------------------------------------------------
    Idea:
      - Same helper isSameTree as Approach 1.
      - Instead of recursing over root, visit its nodes with a BFS queue.
        For each node, ask: is the tree starting at this node identical to
        subRoot? If yes, return True.
      - Push the node's children and keep going. If the queue empties
        without a match, return False.

    Walkthrough on root = 3 -> (4 -> (1, 2), 5), subRoot = 4 -> (1, 2):
        queue [3]:      isSameTree(3, 4) False, push 4 and 5
        queue [4, 5]:   pop 4 -> isSameTree(4, 4) True -> return True

    Why it is the safer choice:
      - The walk over root is a loop, so the depth of root does not matter.
        Only isSameTree is recursive, and its depth is limited by the
        smaller tree (it stops where either tree ends or differs), so it is
        at most the height of subRoot (up to 1000 nodes).
      - Because of the early return, the search stops at the shallowest
        match.

    Time Complexity:  O(m * n) -- same as Approach 1.
    Space Complexity: O(m) -- the queue can hold a whole level of root,
                      which is up to about m / 2 nodes in a complete tree.

    Things to be aware of:
      - This version assumes root is not empty (the constraints guarantee
        at least 1 node). With root = None the queue would start with None
        and `node.left` would raise AttributeError. Add an
        `if root is None: return False` guard if you reuse it elsewhere.
      - A faster option exists: serialize both trees into strings (with
        markers for missing children) and check if one string is a
        substring of the other. That can reach O(m + n) with a linear-time
        substring search, but it is easy to get wrong without the markers.

    Common pitfalls:
      - Forgetting that a match must go all the way down to the leaves.
        isSameTree already does that, so do not replace it with a partial
        comparison.
    """

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def isSameTree(p, q):
            if not p and not q:
                return True
            if not p or not q:
                return False
            if p.val != q.val:
                return False
            return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)

        queue = deque([root])

        while queue:
            node = queue.popleft()

            if isSameTree(node, subRoot):
                return True
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return False