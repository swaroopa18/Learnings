"""
LeetCode 328 - Odd Even Linked List
------------------------------------
Given the head of a singly linked list, group all nodes at ODD positions
together, followed by all nodes at EVEN positions, and return the reordered
list. The first node is position 1 (odd), the second is position 2 (even),
and so on. The relative order inside the odd group and inside the even group
must stay the same. Do it in O(1) extra space and O(n) time.

Note: "odd/even" refers to the node's POSITION (1-based), not its value.

Four approaches are given below.

Summary
-------
 #  Approach                         Time    Space   Notes
 1  Collect nodes in an array        O(n)    O(n)    Easiest to reason about, breaks the O(1) space rule
 2  Two dummy lists (odd / even)     O(n)    O(1)    Very readable, relinks every node once
 3  Odd/even pointers (RECOMMENDED)  O(n)    O(1)    Your version, no extra nodes needed
 4  Recursion                        O(n)    O(n)    Same relinking, uses the call stack

Example:
    1 -> 2 -> 3 -> 4 -> 5   becomes   1 -> 3 -> 5 -> 2 -> 4
"""

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SolutionNodeArray:
    """
    Approach 1: Collect Nodes in an Array
    ---------------------------------------
    Idea:
      - Walk the list once and store every node in a Python list.
      - The odd positions are nodes[0], nodes[2], ...; the even positions
        are nodes[1], nodes[3], ...
      - Build the new order as odd nodes followed by even nodes, relink each
        node to the next one in that order, and set the last node's next to
        None (otherwise the old last node can still point back into the list
        and create a cycle).

    Time Complexity:  O(n) -- one pass to collect, one pass to relink.
    Space Complexity: O(n) -- the array of node references.

    Easy to get right, but it does not meet the problem's O(1) extra space
    requirement. Good as a first idea in an interview before optimizing.
    """

    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        nodes = []
        curr = head
        while curr:
            nodes.append(curr)
            curr = curr.next

        order = nodes[0::2] + nodes[1::2]

        for i in range(len(order) - 1):
            order[i].next = order[i + 1]
        order[-1].next = None

        return order[0]


class SolutionTwoDummyLists:
    """
    Approach 2: Two Dummy Lists (odd list and even list)
    ------------------------------------------------------
    Idea:
      - Build two separate lists as you walk: one for odd positions and one
        for even positions. Each has a dummy head node so appending never
        needs an "is the list empty?" special case.
      - Walk the original list with a position counter. Append the current
        node to the odd tail or the even tail depending on the counter.
      - At the end, cut the even tail (even_tail.next = None) so the last
        even node doesn't still point into the odd list, then attach the
        even list after the odd tail.

    Time Complexity:  O(n) -- every node is visited and relinked once.
    Space Complexity: O(1) -- only two dummy nodes and a few pointers; the
                              real nodes are reused, not copied.

    The dummy-head trick is the standard way to avoid head special cases.
    The only cost compared to Approach 3 is the two extra dummy nodes and a
    counter.
    """

    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        odd_dummy, even_dummy = ListNode(), ListNode()
        odd_tail, even_tail = odd_dummy, even_dummy

        curr = head
        position = 1
        while curr:
            if position % 2 == 1:
                odd_tail.next = curr
                odd_tail = curr
            else:
                even_tail.next = curr
                even_tail = curr
            curr = curr.next
            position += 1

        even_tail.next = None            # cut the tail of the even list
        odd_tail.next = even_dummy.next  # join odd list then even list
        return odd_dummy.next


class Solution:
    """
    Approach 3 (RECOMMENDED): Odd / Even Pointers (in place)
    ----------------------------------------------------------
    Idea:
      - Keep two pointers: `odd` starts at the first node, `even` starts at
        the second. Remember `even_head` (the first even node) because by the
        end the even chain has to be attached after the last odd node.
      - Each loop step "skips over" one node for each pointer:
            odd.next  = odd.next.next     # odd now links to the next odd node
            odd       = odd.next
            even.next = even.next.next    # even now links to the next even node
            even      = even.next
        Since odd.next is always an even node and even.next is always an odd
        node, hopping two nodes at a time strings together the odd chain and
        the even chain at the same time.
      - Stop when `even` or `even.next` is None:
          * odd length  (1 -> 2 -> 3):   even.next is None, odd is last node.
          * even length (1 -> 2 -> 3 -> 4): even itself becomes None.
        In both cases `odd` is sitting on the last odd node.
      - Finish with odd.next = even_head to place the even chain after the
        odd chain. The last even node already has next = None (it came from
        the end of the original list), so no cycle is created.

    Walkthrough on 1 -> 2 -> 3 -> 4 -> 5:
        start:  odd=1, even=2, even_head=2
        step 1: 1 -> 3, odd=3 | 2 -> 4, even=4
        step 2: 3 -> 5, odd=5 | 4 -> None, even=None   (loop ends)
        attach: 5 -> 2          result: 1 -> 3 -> 5 -> 2 -> 4

    Edge cases handled:
      - Empty list or one node: returned as is (nothing to reorder).
      - Two nodes: loop is skipped because even.next is None, then
        odd.next = even_head leaves the list unchanged (1 -> 2).
      - Odd and even lengths both end cleanly through the loop condition.
      - Relative order inside each group is preserved because each group is
        walked left to right.

    Time Complexity:  O(n) -- each node is visited once.
    Space Complexity: O(1) -- only a few pointers, no new nodes.

    Why it's best:
      - It is the optimal solution: O(n) time and O(1) space with no dummy
        nodes or counters.
      - The loop condition `while even and even.next` is all that's needed to
        cover both odd-length and even-length lists.

    Common pitfalls:
      - Looping on `while odd and odd.next` instead; it breaks on even-length
        lists because `even` can become None while odd.next is still set.
      - Forgetting to save `even_head` before the loop (the even chain would
        be lost).
      - Reordering the pointer updates (moving `odd` before updating
        even.next), which corrupts the links.
    """

    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        odd = head
        even = head.next
        even_head = even

        while even and even.next:
            odd.next = odd.next.next
            odd = odd.next

            even.next = even.next.next
            even = even.next

        odd.next = even_head

        return head


class SolutionRecursive:
    """
    Approach 4: Recursion
    -----------------------
    Idea:
      - Same relinking as Approach 3, but each "hop" of the odd and even
        pointers is one recursive call instead of one loop iteration.
      - Base case: when `even` is None or has no next node, the odd chain
        has ended, so attach the saved even_head after `odd` and stop.
      - Recursive case: link odd to the next odd node and even to the next
        even node, then recurse with both pointers advanced.

    Time Complexity:  O(n) -- each node is visited once.
    Space Complexity: O(n) -- recursion depth is about n / 2 frames.

    Not recommended for real use: Python's default recursion limit is 1000,
    so lists with a few thousand nodes would raise RecursionError. It's
    mainly useful to show the recursive structure of the problem.
    """

    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        even_head = head.next

        def relink(odd: ListNode, even: Optional[ListNode]) -> None:
            if not even or not even.next:
                odd.next = even_head
                return
            odd.next = even.next
            even.next = odd.next.next
            relink(odd.next, even.next)

        relink(head, even_head)
        return head