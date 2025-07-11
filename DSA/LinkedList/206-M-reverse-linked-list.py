# https://leetcode.com/problems/reverse-linked-list/description/

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
from typing import Optional

# TC: O(n) SC: O(n)
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        revList = None
        while head:
            node = ListNode(head.val)
            node.next = revList
            revList = node
            head = head.next
        return revList
     

# TC: O(n) SC: O(1)
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        revList = None
        while head:
            temp = head.next
            head.next = revList
            revList = head
            head = temp
        return revList
   

# TC: O(n) SC: O(n)
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        new_head = self.reverseList(head.next)

        head.next.next = head
        head.next = None
        return new_head
    
# TC: O(n) SC: O(n)
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        stack = []
        while head:
            stack.append(head)
            head = head.next
        dummy = ListNode(0)
        curr = dummy
        while stack:
            node = stack.pop()
            curr.next = node
            curr = curr.next
        curr.next = None
        return dummy.next
