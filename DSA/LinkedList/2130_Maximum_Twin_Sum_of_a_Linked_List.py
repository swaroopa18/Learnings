"""
LeetCode 2130 - Maximum Twin Sum of a Linked List
---------------------------------------------------
In a linked list of EVEN length n, the i-th node (0-indexed, i < n / 2) is
the "twin" of node n - 1 - i. The twin sum is the sum of a node's value and
its twin's value. Return the maximum twin sum.

Example:
    5 -> 4 -> 2 -> 1
    twins: (5, 1) and (4, 2) -> sums 6 and 6 -> answer 6

The list length is always even (2 <= n <= 10^5), so the middle splits it into
two equal halves with no middle node to worry about.

The challenge is that a singly linked list can only be walked forward, so we
cannot read from both ends at once. Every approach is a different way of
getting "first half left to right" and "second half right to left" side by
side.

Four approaches are given below.

Summary
-------
 #  Approach                              Time    Space   Notes
 1  Array of values + two pointers        O(n)    O(n)    Simplest, random access does the job
 2  Stack for the first half              O(n)    O(n/2)  Stack gives the reverse order for free
 3  Reverse second half (RECOMMENDED)     O(n)    O(1)    Your version, optimal space
 4  Recursion (compare on the way back)   O(n)    O(n)    Neat, but deep recursion limit in Python
"""

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SolutionArray:
    """
    Approach 1: Array of Values + Two Pointers
    --------------------------------------------
    Idea:
      - Copy all values into a Python list. Now we have random access, so
        twins are simply vals[i] and vals[n - 1 - i].
      - Loop i over the first half and keep the maximum of the sums.

    Time Complexity:  O(n) -- one pass to copy, one pass over the first half.
    Space Complexity: O(n) -- the array of values.

    The easiest solution to write and to trust. Use it first in an interview,
    then mention the O(1)-space version below.
    """

    def pairSum(self, head: Optional[ListNode]) -> int:
        vals = []
        while head:
            vals.append(head.val)
            head = head.next

        n = len(vals)
        return max(vals[i] + vals[n - 1 - i] for i in range(n // 2))


class SolutionStack:
    """
    Approach 2: Stack for the First Half
    --------------------------------------
    Idea:
      - Use slow/fast pointers: while fast moves two steps, slow moves one.
        Push each value slow passes onto a stack, so the stack holds the first
        half of the list.
      - When fast reaches the end, slow is at the start of the second half.
      - Walk the second half forward. The top of the stack (last pushed) is
        the LAST node of the first half, and that is exactly the twin of the
        FIRST node of the second half. So pop one value per step and add.

    Why the order works:
      - First half: a0 a1 a2 | second half: b0 b1 b2
        The stack pops a2, a1, a0 while we walk b0, b1, b2, producing the
        pairs (a2, b0), (a1, b1), (a0, b2). These are exactly the twin pairs
        (index n/2 - 1 - j with index n/2 + j).

    Time Complexity:  O(n)
    Space Complexity: O(n / 2) = O(n) -- the stack.

    Half the memory of Approach 1 and no index arithmetic, but still O(n).
    """

    def pairSum(self, head: Optional[ListNode]) -> int:
        stack = []
        slow = fast = head

        while fast and fast.next:
            stack.append(slow.val)
            slow = slow.next
            fast = fast.next.next

        best = 0
        while slow:
            best = max(best, stack.pop() + slow.val)
            slow = slow.next

        return best


class Solution:
    """
    Approach 3 (RECOMMENDED): Reverse the Second Half In Place
    ------------------------------------------------------------
    Idea:
      1. Find the middle with slow/fast pointers. Because n is even, when
         `fast` falls off the end, `slow` sits on the first node of the
         second half (index n / 2).
      2. Reverse the list starting at `slow`. The second half is now read
         from its last node back to its first node.
      3. Walk `head` (the first half, left to right) and `rev` (the reversed
         second half) together. Each step compares one twin pair:
         head.val + rev.val. Keep the maximum.

    Walkthrough on 5 -> 4 -> 2 -> 1:
        slow/fast: slow ends on node 2 (index 2), fast is None
        reverse from 2:   1 -> 2      (rev points at node 1)
        walk together:    5 + 1 = 6,  4 + 2 = 6   -> max = 6

    Why the loop stops at the right place:
      - After reversing, the old `slow` node (the first node of the second
        half) becomes the TAIL of `rev` with next = None. The last node of
        the first half still points to it, so `head` also ends there. Both
        pointers are walked together for exactly n / 2 steps, and the loop
        ends when `rev` becomes None.

    Time Complexity:  O(n) -- find middle (n/2) + reverse (n/2) + compare (n/2).
    Space Complexity: O(1) -- only pointers.

    Things to be aware of:
      - It MODIFIES the input list (the middle link is reversed). That is
        fine for the judge. If the list must stay intact, reverse the second
        half back after the loop, or use Approach 1 or 2 instead.
      - It relies on the length being even, which the problem guarantees. On
        an odd-length list `slow` would land on the exact middle node and the
        pairing would be off.

    Common pitfalls:
      - Moving `slow` in the reversal loop and then forgetting that it no
        longer points to the middle (use `rev` after the loop, not `slow`).
      - Losing the next node before re-pointing (that's why `temp` is saved
        first).
    """

    def pairSum(self, head: Optional[ListNode]) -> int:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        rev = None
        while slow:
            temp = slow.next
            slow.next = rev
            rev = slow
            slow = temp

        max_val = 0
        while rev:
            max_val = max(head.val + rev.val, max_val)

            head = head.next
            rev = rev.next

        return max_val


class SolutionRecursive:
    """
    Approach 4: Recursion (compare on the way back)
    -------------------------------------------------
    Idea:
      - Recurse all the way to the last node. On the way BACK, the recursion
        visits nodes from the end toward the start, which is the reverse
        order we wanted for free.
      - Keep a `left` pointer that starts at head and moves forward by one
        after every comparison. At each unwind step, `right` is the node
        n - 1 - i and `left` is the node i, so they are twins.
      - Every pair is visited twice (once as (i, n-1-i), once as
        (n-1-i, i)), which is harmless for a maximum.

    Time Complexity:  O(n)
    Space Complexity: O(n) -- call stack depth equals the list length.

    Elegant, but Python's default recursion limit is 1000, so lists of
    thousands of nodes raise RecursionError (n goes up to 10^5 here). Shown
    to illustrate the idea; Approach 3 is the safe choice.
    """

    def pairSum(self, head: Optional[ListNode]) -> int:
        left = head
        best = 0

        def dfs(right: Optional[ListNode]) -> None:
            nonlocal left, best
            if not right:
                return
            dfs(right.next)
            best = max(best, left.val + right.val)
            left = left.next

        dfs(head)
        return best