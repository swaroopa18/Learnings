r"""
LeetCode 112 - Path Sum
-------------------------
Given the root of a binary tree and an integer targetSum, return True if the
tree has a ROOT-TO-LEAF path whose node values add up to targetSum. A leaf is
a node with no children.

Example:
            5
           / \
          4   8
         /   / \
        11  13  4
       /  \      \
      7    2      1
    targetSum = 22 -> path 5 -> 4 -> 11 -> 2 sums to 22 -> True

        1
       / \
      2   3
    targetSum = 1 -> the path 1 alone ends at node 1, which is NOT a leaf.
    Real root-to-leaf sums are 3 and 4 -> False

The key point: the path must start at the root AND end at a leaf. Reaching
the target sum at a node that still has children does not count. Node values
can be negative, so a running sum can go up and down, and we cannot stop
early just because the sum went past the target.

Two approaches are given below.

Summary
-------
 #  Approach                                Time    Space   Notes
 1  Recursion (subtract from the target)    O(n)    O(h)    Shortest code, deep recursion limit in Python
 2  Iterative DFS, stack (RECOMMENDED)      O(n)    O(h)    Your version, carries the running sum, no recursion limit

 (h = height of the tree: O(log n) balanced, O(n) skewed)
"""

from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class SolutionRecursive:
    """
    Approach 1: Recursion (subtract the node value from the target)
    -----------------------------------------------------------------
    Idea:
      - Instead of adding up the path, shrink the target as we go down.
        At each node, the remaining target becomes targetSum - node.val.
      - If the node is a leaf, the path works exactly when the remaining
        target equals the leaf's value (remaining after subtracting is 0).
      - Otherwise the answer is True if EITHER child subtree has a path
        for the reduced target.
      - An empty node (None) returns False, since it has no path.

    Walkthrough on 5 -> 4 -> 11 -> 2 with targetSum = 22:
        at 5:  need 22 - 5  = 17 from below
        at 4:  need 17 - 4  = 13
        at 11: need 13 - 11 = 2
        at 2:  leaf, and 2 - 2 = 0 -> True, passed up through all parents

    Time Complexity:  O(n) -- every node is visited at most once.
    Space Complexity: O(h) -- call stack depth equals the tree height.

    Things to be aware of:
      - The `or` stops as soon as one side returns True, so it can finish
        early when a path is found.
      - For a skewed tree of up to 10^4 nodes (this problem's limit),
        Python's default recursion limit of 1000 can raise RecursionError.
        Approach 2 avoids this.

    Common pitfalls:
      - Returning True when the target hits 0 at a non-leaf node.
      - Treating None as True when the target is 0. A missing child is not a
        leaf, so it must return False. Otherwise a node with one child could
        wrongly succeed through its empty side.
    """

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False

        if not root.left and not root.right:
            return root.val == targetSum

        remaining = targetSum - root.val
        return (self.hasPathSum(root.left, remaining)
                or self.hasPathSum(root.right, remaining))


class Solution:
    """
    Approach 2 (RECOMMENDED): Iterative DFS with a Stack
    ------------------------------------------------------
    Idea:
      - Use an explicit stack in place of recursion. Each stack entry is a
        pair (node, sum of values from the root down to this node).
      - Pop a pair. If the node is a leaf and its running sum equals
        targetSum, a valid path exists, so return True.
      - Otherwise push each existing child with its own running sum
        (current_sum + child.val).
      - If the stack empties with no match, return False.

    Walkthrough on 1 -> (2, 3) with targetSum = 3:
        stack: [(1, 1)]
        pop (1, 1): not a leaf, push (2, 3) and (3, 4)
        pop (3, 4): leaf, 4 != 3
        pop (2, 3): leaf, 3 == 3 -> True

    Why the leaf check matters:
      - Here the root alone has running sum 1. With targetSum = 1 it would
        match if we only compared sums, but the root is not a leaf, so it is
        rejected and the answer is False.

    Time Complexity:  O(n) -- every node is pushed and popped at most once.
    Space Complexity: O(h) -- for a DFS stack the number of pending nodes is
                      bounded by the tree height times a small constant
                      (a node's sibling stays on the stack while we go down).
                      Worst case is still O(n) for a very bushy or skewed
                      tree.

    Things to be aware of:
      - No recursion, so no RecursionError on deep trees.
      - The running sum is stored with each node. That avoids having to
        undo anything when we move to a different branch (no backtracking
        step needed).
      - The original code had an unused `curr = root` line. It does nothing
        and is removed here.

    Common pitfalls:
      - Comparing the sum before checking for a leaf.
      - Forgetting the empty tree case (returns False, even if
        targetSum is 0).
    """

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        stack = [(root, root.val)]

        while stack:
            node, current_sum = stack.pop()
            if not node.left and not node.right and current_sum == targetSum:
                return True
            if node.left:
                stack.append((node.left, current_sum + node.left.val))
            if node.right:
                stack.append((node.right, current_sum + node.right.val))
        return False