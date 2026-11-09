"""
LeetCode 61 - Rotate List
--------------------------
Given the head of a singly linked list, rotate the list to the right by `k`
places and return the new head.

Rotating right by k means the last k nodes move to the front, keeping their
order. Example:
    1 -> 2 -> 3 -> 4 -> 5, k = 2   becomes   4 -> 5 -> 1 -> 2 -> 3

Key observations used by every approach:
  - Rotating by the list length n changes nothing, so only k % n matters.
    (k can be huge, up to 10^9, so never loop k times.)
  - After taking k %= n, the NEW HEAD is the node at index n - k (0-based),
    and the NEW TAIL is the node at index n - k - 1.
  - If k % n == 0 the list is returned untouched.

Four approaches are given below.

Summary
-------
 #  Approach                          Time    Space   Notes
 1  Array of nodes                    O(n)    O(n)    Index arithmetic made trivial, extra space
 2  Length + relink (your version)    O(n)    O(1)    Works, but the second loop is mostly no-ops
 3  Two pointers (fast ahead by k)    O(n)    O(1)    Classic "k-th from the end" pattern
 4  Make it a ring, then cut          O(n)    O(1)    Cleanest idea (RECOMMENDED)
"""

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SolutionNodeArray:
    """
    Approach 1: Array of Nodes
    ----------------------------
    Idea:
      - Walk the list and store every node in a Python list, so we can jump
        to any index directly.
      - With n nodes and k %= n:
            new head = nodes[n - k]
            new tail = nodes[n - k - 1]   -> set its next to None
            old tail = nodes[n - 1]       -> point its next at the old head
      - Return the new head.

    Time Complexity:  O(n) -- one pass to collect, O(1) pointer changes.
    Space Complexity: O(n) -- the array of node references.

    Easiest to reason about, but uses O(n) extra space that the other
    approaches avoid. Good as a first idea before optimizing.
    """

    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        nodes = []
        curr = head
        while curr:
            nodes.append(curr)
            curr = curr.next

        n = len(nodes)
        k %= n
        if k == 0:
            return head

        nodes[n - k - 1].next = None  # cut before the new head
        nodes[-1].next = head         # old tail now points to old head
        return nodes[n - k]


class SolutionLengthAndRelink:
    """
    Approach 2: Length + Relink (your version, annotated)
    -------------------------------------------------------
    Idea:
      - Count the length n and reduce k with k %= n. If k is 0, nothing to do.
      - `slow` walks n - k steps from head. That lands on the node at index
        n - k, which is the NEW HEAD (it is the node we return at the end).
      - `first` starts at `slow` and walks to the old tail (first.next is
        None).
      - The last loop runs n - k times: it sets first.next = second, moves
        `second` forward and moves `first` forward. Starting from the old
        tail, `first` therefore walks through the first n - k original nodes
        (index 0 .. n - k - 1), ending on index n - k - 1, which is the NEW
        TAIL.
      - Finally first.next = None cuts the list after the new tail, and
        `slow` (the new head) is returned.

    What the last loop really does:
      - Only the FIRST iteration changes a link (old tail -> head). In every
        later iteration first.next is already equal to second, so the
        assignment does nothing. The loop is effectively "connect the tail to
        the head, then walk to the new tail". Approach 4 states that directly,
        and saves a pass.

    Walkthrough on 1 -> 2 -> 3 -> 4 -> 5, k = 2:
        n = 5, k = 2, slow moves 3 steps -> slow = node 4 (new head)
        first goes to node 5 (old tail)
        loop x3: 5 -> 1, first = 1 | (1 -> 2 already), first = 2 | (2 -> 3), first = 3
        first = node 3 (new tail), 3 -> None
        result: 4 -> 5 -> 1 -> 2 -> 3

    Edge cases handled:
      - Empty list or one node: returned as is.
      - k == 0 or k a multiple of n: returned unchanged (k %= n gives 0).
      - k larger than n: handled by k %= n.

    Time Complexity:  O(n) -- about 3 passes (count, slow walk, tail walk)
                              plus the relink loop.
    Space Complexity: O(1) -- only pointers.

    Correct and optimal in big-O, just with more walking than needed.
    """

    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        length = 0
        curr = head

        while curr:
            length += 1
            curr = curr.next

        k %= length

        if k == 0:
            return head

        slow = head

        for _ in range(length - k):
            slow = slow.next

        first = slow
        while first.next:
            first = first.next

        second = head
        for _ in range(length - k):
            first.next = second
            second = second.next
            first = first.next

        first.next = None
        return slow


class SolutionTwoPointers:
    """
    Approach 3: Two Pointers (fast is k nodes ahead)
    --------------------------------------------------
    Idea:
      - Count the length n and reduce k with k %= n (needed so that k is
        never larger than the list).
      - Put `fast` k nodes ahead of `slow`. Move both one step at a time
        until fast is on the last node. Now `slow` is exactly k nodes from
        the end, i.e. on the NEW TAIL (index n - k - 1).
      - Then: new_head = slow.next, cut with slow.next = None, and connect
        the old tail with fast.next = head.

    Time Complexity:  O(n) -- one pass to count, one pass for the pointers.
    Space Complexity: O(1)

    This is the standard "k-th node from the end" pattern. It needs the
    length pass only to reduce k; without it, k could run past the end.
    """

    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        n = 0
        curr = head
        while curr:
            n += 1
            curr = curr.next

        k %= n
        if k == 0:
            return head

        fast = slow = head
        for _ in range(k):
            fast = fast.next

        while fast.next:
            slow = slow.next
            fast = fast.next

        new_head = slow.next
        slow.next = None
        fast.next = head
        return new_head


class Solution:
    """
    Approach 4 (RECOMMENDED): Close the List into a Ring, then Cut
    ----------------------------------------------------------------
    Idea:
      - In ONE pass, find both the length n and the old tail.
      - Link the tail back to the head (tail.next = head). The list is now
        a ring, and rotating a ring is just choosing where to cut it.
      - Reduce k with k %= n. The new tail is the node at index n - k - 1, so
        walk n - k - 1 steps from head to reach it.
      - The new head is new_tail.next. Cut the ring with new_tail.next = None
        and return the new head.

    Walkthrough on 1 -> 2 -> 3 -> 4 -> 5, k = 2:
        n = 5, tail = node 5, make the ring: 5 -> 1
        k %= 5 -> 2, walk 5 - 2 - 1 = 2 steps from head -> new tail = node 3
        new head = 3.next = node 4, cut 3 -> None
        result: 4 -> 5 -> 1 -> 2 -> 3

    Edge cases handled:
      - Empty list or one node: returned as is.
      - k == 0 or k a multiple of n: return head BEFORE closing the ring, so
        we never leave a cycle behind.
      - k much larger than n (e.g. 2 * 10^9): handled by k %= n.

    Time Complexity:  O(n) -- one pass to measure, one walk to the cut point.
    Space Complexity: O(1)

    Why it's best:
      - One clear idea (ring, then cut) with no helper pointers racing each
        other and no leftover no-op loop.
      - The length and tail come from a single traversal.

    Common pitfalls:
      - Forgetting k %= n (TLE or wrong answer for huge k).
      - Walking n - k steps instead of n - k - 1 (cuts one node too late).
      - Not breaking the ring (new_tail.next = None), which leaves a cycle
        and makes the judge loop forever.
    """

    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        n = 1
        tail = head
        while tail.next:
            tail = tail.next
            n += 1

        k %= n
        if k == 0:
            return head

        tail.next = head  # close the ring

        new_tail = head
        for _ in range(n - k - 1):
            new_tail = new_tail.next

        new_head = new_tail.next
        new_tail.next = None  # break the ring
        return new_head