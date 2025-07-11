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
   