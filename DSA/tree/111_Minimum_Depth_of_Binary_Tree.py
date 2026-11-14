"""
LeetCode 111 - Minimum Depth of Binary Tree
---------------------------------------------
The minimum depth is the number of nodes along the shortest path from the
root down to the nearest LEAF. A leaf is a node with no children. An empty
tree has depth 0.

Example:
        3
       / \
      9  20
         / \
        15  7
    nearest leaf is 9 (path 3 -> 9) -> answer 2

        2
         \
          3
           \
            4
    node 2 has only a right child, so it is NOT a leaf. The only leaf is 4
    (path 2 -> 3 -> 4) -> answer 3, not 1.

The key point: the path must end at a leaf. A node with one missing child
does not count as the end of a path, so the missing side must be ignored
instead of being treated as depth 0. This is the classic trap, and the
reason this problem is not just "min instead of max" from Maximum Depth.

Two approaches are given below.

Summary
-------
 #  Approach                              Time    Space   Notes
 1  BFS level by level (RECOMMENDED)      O(n)    O(w)    Stops at the first leaf, no need to see the whole tree
 2  DFS recursion                         O(n)    O(h)    Visits every node, needs the one-child special case

 (w = max width of the tree, h = height of the tree)
"""

from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """
    Approach 1 (RECOMMENDED): BFS Level by Level
    ----------------------------------------------
    Idea:
      - Walk the tree one level at a time with a queue, counting levels.
      - The first leaf we meet is on the shallowest level that has a leaf,
        so that level number is the answer. Return right away.
      - A node is a leaf only if it has neither a left nor a right child.

    Walkthrough on 3 -> (9, 20 -> (15, 7)):
        level 1: [3]        3 is not a leaf, add 9 and 20
        level 2: [9, 20]    9 is a leaf -> return 2

    Walkthrough on 2 -> right 3 -> right 4:
        level 1: [2]   not a leaf (has a right child)
        level 2: [3]   not a leaf
        level 3: [4]   leaf -> return 3

    Why BFS fits this problem:
      - BFS reaches nodes in order of depth, so the first leaf found is
        guaranteed to be the closest one. There is no need to look at the
        rest of the tree.
      - Because it checks "no left AND no right", the one-child trap is
        handled naturally. A node with one child is simply not a leaf and
        the search continues below it.

    Time Complexity:  O(n) worst case (when the nearest leaf is on the
                      last level), but often much less because it stops
                      early.
    Space Complexity: O(w) -- the queue holds at most one level, which is
                      up to about n / 2 nodes in a complete tree.

    Things to be aware of:
      - The final `return level` after the loop is never reached for a
        non-empty tree, since every tree has at least one leaf and the loop
        returns when it finds it. It is only there to satisfy the function
        shape.

    Common pitfalls:
      - Forgetting the empty tree check (answer is 0).
      - Counting a node with one child as a leaf.
    """

    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        queue = deque([root])
        level = 0
        while queue:
            level += 1
            count = len(queue)
            for _ in range(count):
                node = queue.popleft()
                if not node.left and not node.right:
                    return level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return level


class SolutionDFS:
    """
    Approach 2: DFS Recursion (with the one-child special case)
    -------------------------------------------------------------
    Idea:
      - dfs(node) returns the minimum depth of the subtree at `node`.
      - Base cases:
          * node is None        -> 0
          * node is a leaf      -> 1
      - For a node with BOTH children, the answer is 1 + min(left, right).
      - For a node with only ONE child, the missing side must not be used in
        the min. Otherwise it would give 0 and make the node look like a
        leaf. So take the depth of the side that exists: 1 + that side.

    Walkthrough on 2 -> right 3 -> right 4:
        dfs(4) = 1                       (leaf)
        dfs(3): no left   -> 1 + dfs(4) = 2
        dfs(2): no left   -> 1 + dfs(3) = 3

    What goes wrong without the special case:
      - With plain `1 + min(left, right)`, node 2 would compute
        1 + min(0, 2) = 1, which is wrong (the answer is 3).

    Time Complexity:  O(n) -- every node is visited once. Unlike BFS it
                      cannot stop at the first leaf.
    Space Complexity: O(h) -- recursion depth equals the tree height
                      (O(log n) balanced, O(n) skewed).

    Things to be aware of:
      - For a very skewed tree of 10^5 nodes, Python's default recursion
        limit (1000) can raise RecursionError. BFS has no such problem.
      - The outer `if root is None: return 0` is already covered by the
        base case inside dfs, so it is optional.

    Common pitfalls:
      - Using min(left, right) when one child is missing.
      - Checking only `not node.left` and forgetting the symmetric
        `not node.right` case.
    """

    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        def dfs(node):
            if node is None:
                return 0
            if not node.left and not node.right:
                return 1
            left = dfs(node.left)
            right = dfs(node.right)

            if not node.left:
                return 1 + right
            if not node.right:
                return 1 + left

            return 1 + min(left, right)

        return dfs(root)